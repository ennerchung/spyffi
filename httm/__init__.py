# See https://docs.python.org/2/library/collections.html#collections.namedtuple for details
from collections import namedtuple

Parameters = namedtuple(
    'Parameters',
    [
        'number_of_slices',  # number of slices to use in transformation, either 1 or 4
        'video_scale',  # electrons/ADU
        'compression',
        'baseline_adu',  # parameter only for calibrated->raw, derived from data for raw->calibrated
        'drift_adu',  # parameter only for calibrated->raw
        'start_of_line_ringing',  # array of length 534, parameter only for calibrated->raw
        'undershoot',
        'smear_ratio',
        'clip_level_adu',
        'pattern_noise'  # 2D array, slice dimensions (2078 by 534)
    ])

FITSData = namedtuple(
    'FITSData',
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
     'parameters',
     'pixel_data'])

RAWTransformation = namedtuple(
    'RAWTransformation',
    ['number_of_slices'])

CalibratedTransformation = namedtuple(
    'CalibratedTransformation',
    ['number_of_slices'])


def make_slice_from_calibrated_data(pixel_data, index, parameters):
    """Construct a slice from an array of calibrated pixel data and a specified index"""
    return Slice(pixel_data=pixel_data,
                 index=index,
                 parameters=parameters,
                 unit='electrons')


def calibrated_transform_from_hdulist(hdulist, number_of_slices=4, **kwargs):
    """Construct a CalibratedTransformation from an astropy.io.fits.HDUList"""
    from numpy import hsplit
    assert len(hdulist) == 1, "Only a single image per FITS file is supported"
    assert hdulist[0].data.shape[1] % number_of_slices == 0, \
        "Image did not have the specified number of slices"
    parameters = Parameters(number_of_slices=number_of_slices, **kwargs)
    return CalibratedTransformation(
        slices=map(lambda pixel_data, index:
                   make_slice_from_calibrated_data(pixel_data, index, parameters),
                   zip(hsplit(hdulist[0].data, number_of_slices), range(number_of_slices))))


def calibrated_transform_from_file(file_name, **kwargs):
    """Construct a CalibratedTransformation from a file or file name"""
    from astropy.io import fits
    return calibrated_transform_from_hdulist(fits.open(file_name), **kwargs)


def make_slice_from_raw_data(pixel_data, index, parameters):
    """Construct a slice from an array of calibrated pixel data and a specified index"""
    return Slice(pixel_data=pixel_data,
                 index=index,
                 parameters=parameters,
                 unit='electrons')


def raw_transform_from_hdulist(hdulist, number_of_slices=4, **kwargs):
    """Construct a RAWTransformation from an astropy.io.fits.HDUList"""
    from numpy import hsplit
    assert len(hdulist) == 1, "Only a single image per FITS file is supported"
    assert hdulist[0].data.shape[1] % number_of_slices == 0, \
        "Image did not have the specified number of slices"
    parameters = Parameters(number_of_slices=number_of_slices, **kwargs)
    return RAWTransformation(
        slices=map(lambda pixel_data, index:
                   make_slice_from_raw_data(pixel_data, index, parameters),
                   zip(hsplit(hdulist[0].data, number_of_slices), range(number_of_slices))))


def raw_transform_from_file(file_name, **kwargs):
    """Construct a RAWTransformation from a file or file name"""
    from astropy.io import fits
    return raw_transform_from_hdulist(fits.open(file_name), **kwargs)