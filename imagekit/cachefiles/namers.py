"""
Functions responsible for returning filenames for the given image generator.
Users are free to define their own functions; these are just some some sensible
choices.

"""

from django.conf import settings
import os
from ..utils import format_to_extension, suggest_extension


def source_name_as_path(generator):
    """
    A namer that, given the following source file name::

        photos/thumbnails/bulldog.jpg

    will generate a name like this::

        /path/to/generated/images/photos/thumbnails/bulldog/5ff3233527c5ac3e4b596343b440ff67.jpg

    where "/path/to/generated/images/" is the value specified by the
    ``IMAGEKIT_CACHEFILE_DIR`` setting.

    """
    source_filename = getattr(generator.source, 'name', None)

    if source_filename is None or os.path.isabs(source_filename):
        # Generally, we put the file right in the cache file directory.
        dir = settings.IMAGEKIT_CACHEFILE_DIR
    else:
        # For source files with relative names (like Django media files),
        # use the source's name to create the new filename.
        dir = os.path.join(settings.IMAGEKIT_CACHEFILE_DIR,
                           os.path.splitext(source_filename)[0])

    ext = suggest_extension(source_filename or '', generator.format)
    return os.path.normpath(os.path.join(dir,
                                         '%s%s' % (generator.get_hash(), ext)))


def source_name_dot_hash(generator):
    """
    A namer that, given the following source file name::

        photos/thumbnails/bulldog.jpg

    will generate a name like this::

        /path/to/generated/images/photos/thumbnails/bulldog.5ff3233527c5.jpg

    where "/path/to/generated/images/" is the value specified by the
    ``IMAGEKIT_CACHEFILE_DIR`` setting.

    """
    source_filename = getattr(generator.source, 'name', None)

    if source_filename is None or os.path.isabs(source_filename):
        # Generally, we put the file right in the cache file directory.
        dir = settings.IMAGEKIT_CACHEFILE_DIR
    else:
        # For source files with relative names (like Django media files),
        # use the source's name to create the new filename.
        dir = os.path.join(settings.IMAGEKIT_CACHEFILE_DIR,
                           os.path.dirname(source_filename))

    ext = suggest_extension(source_filename or '', generator.format)
    basename = os.path.basename(source_filename)
    return os.path.normpath(os.path.join(dir, '%s.%s%s' % (
            os.path.splitext(basename)[0], generator.get_hash()[:12], ext)))


def hash(generator):
    """
    A namer that, given the following source file name::

        photos/thumbnails/bulldog.jpg

    will generate a name like this::

        /path/to/generated/images/5ff3233527c5ac3e4b596343b440ff67.jpg

    where "/path/to/generated/images/" is the value specified by the
    ``IMAGEKIT_CACHEFILE_DIR`` setting.

    """
    format = getattr(generator, 'format', None)
    ext = format_to_extension(format) if format else ''
    return os.path.normpath(os.path.join(settings.IMAGEKIT_CACHEFILE_DIR,
                                         '%s%s' % (generator.get_hash(), ext)))

def cache_dir_source_name(generator):
    """
    A namer that, given the following source file name::

        photos/thumbnails/bulldog.jpg

    will generate a name like this::

        /path/to/generated/images/cache_dir/photos/thumbnails/bulldog.jpg

    where "/path/to/generated/images/" is the value specified by the
    ``IMAGEKIT_CACHEFILE_DIR`` setting and "cache_dir" is the value 
    specified by ``ImageSpecField`` keyword argument.

    NB The user is responsible of choosing cache_dir unique enough to 
    avoid collisions!

    """
    source_filename = getattr(generator.source, 'name', None)
    basename = source_filename.replace(generator.source.field.upload_to, '').lstrip(os.path.sep)
    dir = settings.IMAGEKIT_CACHEFILE_DIR
    subdir = generator.cache_dir
    return os.path.normpath(os.path.join(dir, subdir, basename))
 

