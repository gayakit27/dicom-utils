import numpy as np
import pydicom
from pydicom.uid import generate_uid
from pydicom.dataset import Dataset
from pydicom.sequence import Sequence
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import pandas as pd
import os
import scipy.ndimage
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import vtk


# function that returns the full file path
def find_file_with_prefix(folder_path, prefix):
    for file_name in os.listdir(folder_path):
        if file_name.startswith(prefix):
            return os.path.join(folder_path, file_name)
    return None


# getting the full file path
def read_dicom_rs_file(file_path):
    ds = pydicom.dcmread(file_path)
    if ds.Modality == 'RTSTRUCT':
        return ds
    else:
        raise ValueError("The provided file is not an RT Structure Set (RTSTRUCT) DICOM file.")


def read_dicom_rd_file(file_path):
    ds = pydicom.dcmread(file_path)
    if ds.Modality == 'RTDOSE':
        return ds
    else:
        raise ValueError("The provided file is not a Radiation Dose (RD) DICOM file.")


def read_dicom_CT_file(file_path):
    ct = pydicom.dcmread(file_path)
    if ct.Modality == 'CT':
        return ct
    else:
        raise ValueError("The provided file is not a CT DICOM file.")


def get_contour_data(rs_dataset):
    contour_data = {}
    roi_contour_sequence = rs_dataset.ROIContourSequence

    for roi_contour in roi_contour_sequence:
        roi_name = "Unknown ROI"  # Default ROI name if ROIName is not present
        if hasattr(roi_contour, 'ROIName'):
            roi_name = roi_contour.ROIName

        contour_data[roi_name] = []

        contour_sequence = roi_contour.ContourSequence
        for contour_sequence_item in contour_sequence:
            contour_points = contour_sequence_item.ContourData
            contour_data[roi_name].append(contour_points)

    return contour_data


def plot_contour(rs_dataset):
    fig, ax = plt.subplots()

    for roi_contour in rs_dataset.ROIContourSequence:
        roi_name = roi_contour.ROIName if hasattr(roi_contour, 'ROIName') else "Unknown ROI"

        for contour_sequence_item in roi_contour.ContourSequence:
            contour_points = np.array(contour_sequence_item.ContourData).reshape(-1, 3)
            contour_points_data = contour_points

            contour_points = contour_points[:, :2]  # Ignore Z coordinate

            polygon = Polygon(contour_points, closed=True, edgecolor='r', facecolor='none')
            ax.add_patch(polygon)

    ax.set_aspect('equal', 'box')
    ax.autoscale_view()
    ax.invert_yaxis()
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Contour Plot')
    plt.show()


def get_radiation_maps(folder_path):
    RS_file_name = find_file_with_prefix(folder_path, 'RS')
    RD_file_name = find_file_with_prefix(folder_path, 'RD')
    RS_data = read_dicom_rs_file(RS_file_name)
    print(RS_data)
    plot_contour(RS_data)

    RD_data = read_dicom_rd_file(RD_file_name)

    voxels = RD_data.pixel_array
    z_size = voxels.shape[2]

    dose_map_array_list = []
    for i in range(0, z_size):
        dose_map_array_list.append(voxels[:, :, i])
