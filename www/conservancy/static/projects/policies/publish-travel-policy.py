#!/usr/bin/env python3

import argparse
import contextlib
import functools
import locale
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

try:
    import markdown
    from markdown.extensions import tables as mdx_tables
    from markdown.extensions import sane_lists as mdx_sane_lists
    from markdown.extensions import smarty as mdx_smarty
    from markdown.extensions import toc as mdx_toc
    markdown_import_success = True
except ImportError:
    if __name__ != '__main__':
        raise
    markdown_import_success = False

TEMPLATE_HEADER = """{% extends "base_projects.html" %}
{% block subtitle %}Travel and Reimburseable Expense Policy - {% endblock %}
{% block submenuselection %}Policies{% endblock %}
{% block content %}

"""

TEMPLATE_FOOTER = """

{% endblock %}
"""

@contextlib.contextmanager
def run(cmd, encoding=None, ok_exitcodes=frozenset([0]), **kwargs):
    kwargs.setdefault('stdout', subprocess.PIPE)
    if encoding is None:
        mode = 'rb'
        no_data = b''
    else:
        mode = 'r'
        no_data = ''
    with contextlib.ExitStack() as exit_stack:
        proc = exit_stack.enter_context(subprocess.Popen(cmd, **kwargs))
        pipes = [exit_stack.enter_context(open(
                   getattr(proc, name).fileno(), mode, encoding=encoding, closefd=False))
                 for name in ['stdout', 'stderr']
                 if kwargs.get(name) is subprocess.PIPE]
        if pipes:
            yield (proc, *pipes)
        else:
            yield proc
        for pipe in pipes:
            for _ in iter(lambda: pipe.read(4096), no_data):
                pass
    if proc.returncode not in ok_exitcodes:
        raise subprocess.CalledProcessError(proc.returncode, cmd)

class GitPath:
    GIT_BIN = shutil.which('git')
    CLEAN_ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    ANY_EXITCODE = range(-256, 257)
    IGNORE_ERRORS = {
        'ok_exitcodes': ANY_EXITCODE,
        'stderr': subprocess.DEVNULL,
    }
    STATUS_CLEAN_OR_UNMANAGED = frozenset(' ?')

    def __init__(self, path, encoding, env=None):
        self.path = path
        self.dir_path = path if path.is_dir() else path.parent
        self.encoding = encoding
        self.run_defaults = {
            'cwd': str(self.dir_path),
            'env': env,
        }

    @classmethod
    def can_run(cls):
        return cls.GIT_BIN is not None

    def _run(self, cmd, encoding=None, ok_exitcodes=frozenset([0]), **kwargs):
        return run(cmd, encoding, ok_exitcodes, **self.run_defaults, **kwargs)

    def _cache(orig_func):
        attr_name = '_cached_' + orig_func.__name__
        @functools.wraps(orig_func)
        def cache_wrapper(self):
            try:
                return getattr(self, attr_name)
            except AttributeError:
                setattr(self, attr_name, orig_func(self))
                return getattr(self, attr_name)
        return cache_wrapper

    @_cache
    def is_work_tree(self):
        with self._run([self.GIT_BIN, 'rev-parse', '--is-inside-work-tree'],
                       self.encoding, **self.IGNORE_ERRORS) as (_, stdout):
            return stdout.readline() == 'true\n'

    @_cache
    def status_lines(self):
        with self._run([self.GIT_BIN, 'status', '-z'],
                       self.encoding) as (_, stdout):
            return stdout.read().split('\0')

    @_cache
    def has_managed_modifications(self):
        return any(line and line[1] not in self.STATUS_CLEAN_OR_UNMANAGED
                   for line in self.status_lines())

    @_cache
    def has_staged_changes(self):
        return any(line and line[0] not in self.STATUS_CLEAN_OR_UNMANAGED
                   for line in self.status_lines())

    def commit_at(self, revision):
        with self._run([self.GIT_BIN, 'rev-parse', revision],
                       self.encoding) as (_, stdout):
            return stdout.readline().rstrip('\n') or None

    @_cache
    def upstream_commit(self):
        return self.commit_at('@{upstream}')

    @_cache
    def head_commit(self):
        return self.commit_at('HEAD')

    def in_sync_with_upstream(self):
        return self.upstream_commit() == self.head_commit()

    @_cache
    def last_commit(self):
        with self._run([self.GIT_BIN, 'log', '-n1', '--format=format:%H', self.path.name],
                       self.encoding, **self.IGNORE_ERRORS) as (_, stdout):
            return stdout.readline().rstrip('\n') or None

    def operate(self, subcmd, ok_exitcodes=frozenset([0])):
        with self._run([self.GIT_BIN, *subcmd], None, ok_exitcodes, stdout=None):
            pass


def add_parser_flag(argparser, dest, **kwargs):
    kwargs.update(dest=dest, default=None)
    switch_root = dest.replace('_', '-')
    switch = '--' + switch_root
    argparser.add_argument(switch, **kwargs, action='store_true')
    kwargs['help'] = "Do not do {}".format(switch)
    argparser.add_argument('--no-' + switch_root, **kwargs, action='store_false')

def parse_arguments(arglist):
    parser = argparse.ArgumentParser(
        epilog="""By default, the program will pull from Git if the output path
is a Git checkout with a tracking branch, and will commit and push if
that checkout is in sync with the tracking branch without any staged changes.
Setting any flag will always override the default behavior.
""",
    )

    parser.add_argument(
        '--encoding', '-E',
        default=locale.getpreferredencoding(),
        help="Encoding to use for all I/O. "
        "Default is your locale's encoding.",
    )
    parser.add_argument(
        '--revision', '-r',
        help="Revision string to version the published page. "
        "Default determined from the revision of the source file.",
    )
    add_parser_flag(
        parser, 'pull',
        help="Try to pull the remote tracking branch to make the checkout "
        "up-to-date before making changes"
    )
    add_parser_flag(
        parser, 'commit',
        help="Commit changes to the travel policy",
    )
    parser.add_argument(
        '-m', dest='commit_message',
        default="Publish {filename} revision {revision}.",
        help="Message for any commit",
    )
    add_parser_flag(
        parser, 'push',
        help="Push to the remote tracking branch after committing changes",
    )
    parser.add_argument(
        'input_path', type=pathlib.Path,
        help="Path to the Conservancy travel policy Markdown source",
    )
    parser.add_argument(
        'output_path', type=pathlib.Path,
        nargs='?', default=pathlib.Path(__file__).parent,
        help="Path to the directory to write output files",
    )

    if not markdown_import_success:
        parser.error("""markdown module is not installed.
Try `apt install python3-markdown` or `python3 -m pip install --user Markdown`.""")

    args = parser.parse_args(arglist)
    args.git_output = GitPath(args.output_path, args.encoding)
    if args.pull or args.commit or args.push:
        if not args.git_output.can_run():
            parser.error("Git operation requested but `git` not found in PATH")
        elif not args.git_output.is_work_tree():
            parser.error("Git operation requested but {} is not a working path".format(
                args.output_path.as_posix()))
    if args.revision is None:
        try:
            args.revision = GitPath(args.input_path, args.encoding, GitPath.CLEAN_ENV).last_commit()
        except subprocess.CalledProcessError:
            pass
        if args.revision is None:
            parser.error("no --revision specified and not found from input path")
    args.output_link_path = args.git_output.dir_path / 'conservancy-travel-policy.html'
    args.output_file_path = args.output_link_path.with_suffix('.{}.html'.format(args.revision))
    return args

class GitOperation:
    def __init__(self, args):
        self.args = args
        self.git_path = args.git_output
        self.exitcode = None
        self.on_work_tree = self.git_path.can_run() and self.git_path.is_work_tree()

    def run(self):
        arg_state = getattr(self.args, self.NAME)
        if arg_state is None:
            arg_state = self.should_run()
        if not arg_state:
            return
        try:
            self.exitcode = self.run_git() or 0
        except subprocess.CalledProcessError as error:
            self.exitcode = error.returncode


class GitPull(GitOperation):
    NAME = 'pull'

    def should_run(self):
        return self.on_work_tree and not self.git_path.has_staged_changes()

    def run_git(self):
        self.git_path.operate(['fetch', '--no-tags'])
        self.git_path.operate(['merge', '--ff-only'])


class GitCommit(GitOperation):
    NAME = 'commit'
    VERB = 'committed'

    def __init__(self, args):
        super().__init__(args)
        try:
            self._should_run = ((not self.git_path.has_staged_changes())
                                and self.git_path.in_sync_with_upstream())
        except subprocess.CalledProcessError:
            self._should_run = False

    def should_run(self):
        return self.on_work_tree and self._should_run

    def run_git(self):
        self.git_path.operate([
            'add', str(self.args.output_file_path), str(self.args.output_link_path),
        ])
        commit_message = self.args.commit_message.format(
            filename=self.args.output_link_path.name,
            revision=self.args.revision,
        )
        self.git_path.operate(['commit', '-m', commit_message])


class GitPush(GitCommit):
    NAME = 'push'
    VERB = 'pushed'

    def run_git(self):
        self.git_path.operate(['push'])


def write_output(args):
    converter = markdown.Markdown(
        extensions=[
            mdx_tables.TableExtension(),
            mdx_sane_lists.SaneListExtension(),
            mdx_smarty.SmartyExtension(),
            mdx_toc.TocExtension(),
        ],
        output_format='html5',
    )
    with args.input_path.open(encoding=args.encoding) as src_file:
        body = converter.convert(src_file.read())
    with tempfile.NamedTemporaryFile(
            'w',
            encoding=args.encoding,
            dir=args.git_output.dir_path.as_posix(),
            suffix='.html',
            delete=False,
    ) as tmp_out:
        try:
            tmp_out.write(TEMPLATE_HEADER)
            tmp_out.write(body)
            tmp_out.write(TEMPLATE_FOOTER)
            tmp_out.flush()
            os.rename(tmp_out.name, str(args.output_file_path))
        except BaseException:
            os.unlink(tmp_out.name)
            raise
    if args.output_link_path.is_symlink():
        args.output_link_path.unlink()
    args.output_link_path.symlink_to(args.output_file_path.name)

def main(arglist=None, stdout=sys.stdout, stderr=sys.stderr):
    args = parse_arguments(arglist)
    pull = GitPull(args)
    pull.run()
    if pull.exitcode:
        return pull.exitcode
    write_output(args)
    ops = [GitCommit(args), GitPush(args)]
    for op in ops:
        op.run()
        if op.exitcode != 0:
            exitcode = op.exitcode or 0
            break
    else:
        exitcode = 0
    print(args.input_path.name, "converted,",
          ", ".join(op.VERB if op.exitcode == 0 else "not " + op.VERB for op in ops),
          file=stdout)
    return exitcode

if __name__ == '__main__':
    exit(main())

