# See https://docs.python.org/2/library/collections.html#collections.namedtuple for details
from collections import namedtuple

CalibratedTransformParameters = namedtuple(
    'CalibratedTransformParameters',
    [
        'number_of_slices',  # number of slices to use in transformation, either 1 or 4
        'video_scale',  # electrons/ADU
        'compression',
        'baseline_adu',
        'drift_adu',
        'start_of_line_ringing',
        'undershoot',
        'smear_ratio',
        'clip_level_adu',
        'pattern_noise'  # 2D array, slice dimensions (2078 by 534)
    ])
CalibratedTransformParameters.__new__.__defaults__ = (None,) * len(CalibratedTransformParameters._fields)

RAWTransformParameters = namedtuple(
    'RAWTransformParameters',
    [
        'number_of_slices',  # number of slices to use in transformation, either 1 or 4
        'video_scale',  # electrons/ADU
        'compression',
        'undershoot',
        'smear_ratio',
        'clip_level_adu',
        'pattern_noise'  # 2D array, slice dimensions (2078 by 534)
    ])
RAWTransformParameters.__new__.__defaults__ = (None,) * len(RAWTransformParameters._fields)

FITSMetaData = namedtuple(
    'FITSMetaData',
    ['origin_file_name',
     'header'])

Slice = namedtuple(
    'Slice',
    ['index',
     'units',
     'image_pixels',
     'smear_rows',
     'top_dark_pixels_rows',
     'left_dark_pixels_columns',
     'right_dark_pixels_columns',
     'pixel_data'])
Slice.__new__.__defaults__ = (None,) * len(Slice._fields)

RAWTransformation = namedtuple(
    'RAWTransformation',
    ['slices',
     'fits_metadata',
     'parameters'])

CalibratedTransformation = namedtuple(
    'CalibratedTransformation',
    ['slices',
     'fits_metadata',
     'parameters'])


def write_calibrated_fits(output_file, raw_transform):
    from astropy.io.fits import HDUList, PrimaryHDU
    from numpy import hstack
    # noinspection PyTypeChecker
    HDUList(PrimaryHDU(header=raw_transform.fits_metadata.header,
                       data=hstack([calibrated_slice.pixel_data
                                    for calibrated_slice in raw_transform.slices]))).writeto(output_file)


def write_raw_fits(output_file, calibrated_transform):
    from astropy.io.fits import HDUList, PrimaryHDU
    from numpy import hstack
    # noinspection PyTypeChecker
    HDUList(PrimaryHDU(header=calibrated_transform.fits_metadata.header,
                       data=hstack([raw_slice.pixel_data
                                    for raw_slice in calibrated_transform.slices]))).writeto(output_file)


def make_slice_from_calibrated_data(pixel_data, index):
    """Construct a slice from an array of calibrated pixel data and a specified index"""
    return Slice(pixel_data=pixel_data,
                 index=index,
                 units='electrons')


def calibrated_transform_from_file(input_file, number_of_slices=4, **kwargs):
    """Construct a CalibratedTransformation from a file or file name"""
    from astropy.io import fits
    from numpy import hsplit
    header_data_unit_list = fits.open(input_file)
    assert len(header_data_unit_list) == 1, "Only a single image per FITS file is supported"
    assert header_data_unit_list[0].data.shape[1] % number_of_slices == 0, \
        "Image did not have the specified number of slices"
    origin_file_name = None
    if isinstance(input_file, basestring):
        origin_file_name = input_file
    if hasattr(input_file, 'name'):
        origin_file_name = input_file.name
    return CalibratedTransformation(
        slices=map(lambda (pixel_data, index):
                   make_slice_from_calibrated_data(pixel_data, index),
                   zip(hsplit(header_data_unit_list[0].data, number_of_slices), range(number_of_slices))),
        fits_metadata=FITSMetaData(origin_file_name=origin_file_name,
                                   header=header_data_unit_list[0].header),
        parameters=CalibratedTransformParameters(number_of_slices=number_of_slices, **kwargs))


def make_slice_from_raw_data(pixel_data, index):
    """Construct a slice from an array of calibrated pixel data and a specified index"""
    return Slice(pixel_data=pixel_data,
                 index=index,
                 units='hdu')


def raw_transform_from_file(input_file, number_of_slices=4, **kwargs):
    """Construct a RAWTransformation from a file or file name"""
    from astropy.io import fits
    from numpy import hsplit
    header_data_unit_list = fits.open(input_file)
    assert len(header_data_unit_list) == 1, "Only a single image per FITS file is supported"
    assert header_data_unit_list[0].data.shape[1] % number_of_slices == 0, \
        "Image did not have the specified number of slices"
    origin_file_name = None
    if isinstance(input_file, basestring):
        origin_file_name = input_file
    if hasattr(input_file, 'name'):
        origin_file_name = input_file.name
    return RAWTransformation(
        slices=map(lambda (pixel_data, index):
                   make_slice_from_raw_data(pixel_data, index),
                   zip(hsplit(header_data_unit_list[0].data, number_of_slices), range(number_of_slices))),
        fits_metadata=FITSMetaData(origin_file_name=origin_file_name,
                                   header=header_data_unit_list[0].header),
        parameters=RAWTransformParameters(number_of_slices=number_of_slices, **kwargs))
