def organize_media_by_event(eventmedia_queryset):
    """Organizes event media by event.

    Given a queryset of event media, it returns a list of 'objects'
    with the following properties:

    * event (event object)
    * date (date object for most recently posted media from event)
    * media_list (a string of the available media types)
    """

    media_by_event = {}
    for media in eventmedia_queryset:
        media_by_event.setdefault(media.event.id, []).append(media)
    mbe = [{'event': x[0].event,
            'date': max(y.date_created for y in x),
            'media_list': ', '.join(set(y.get_format_display() for y in x))}
           for x in media_by_event.values()]
    mbe.sort(key=(lambda x: x['date']), reverse=True) # sort by date
    return mbe
