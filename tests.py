import os
from dicom_utils import find_file_with_prefix, read_dicom_rs_file, read_dicom_rd_file, get_contour_data, \
    read_dicom_CT_file, plot_contour, get_radiation_maps

EXAMPLE_FOLDER_Radiation_Plans = r"C:\Users\USER\Documents\dicom-utils\data\7227_Radiation plans_27102021\7227_Radiation plans_27102021"
EXAMPLE_FOLDER_CT = r"C:\Users\USER\Documents\dicom-utils\data\7227_anatomyCT_27102021\7227_FSR_RT Hipocampus_27102021"


def test_find_file_with_prefix():
    RS_file_path = find_file_with_prefix(EXAMPLE_FOLDER_Radiation_Plans, 'RS')


def test_read_dicom_files():
    RD_file_path = find_file_with_prefix(EXAMPLE_FOLDER_Radiation_Plans, 'RD')
    RS_file_path = find_file_with_prefix(EXAMPLE_FOLDER_Radiation_Plans, 'RS')
    CT_file_path = find_file_with_prefix(EXAMPLE_FOLDER_CT, 'CT')
    RS_data = read_dicom_rs_file(RS_file_path)
    RD_data = read_dicom_rd_file(RD_file_path)
    CT_data = read_dicom_CT_file(CT_file_path)


def test_get_contour_data():
    RS_file_path = find_file_with_prefix(EXAMPLE_FOLDER_Radiation_Plans, 'RS')
    RS_data = read_dicom_rs_file(RS_file_path)
    contour_data = get_contour_data(RS_data)


def test_plot_contour():
    RS_file_path = find_file_with_prefix(EXAMPLE_FOLDER_Radiation_Plans, 'RS')
    RS_data = read_dicom_rs_file(RS_file_path)
    plot_contour(RS_data)


def test_get_radiation_maps():
    RS_file_path = find_file_with_prefix(EXAMPLE_FOLDER_Radiation_Plans, 'RS')
    RS_data = read_dicom_rs_file(RS_file_path)
    get_radiation_maps(RS_data)


def test_all():
    test_find_file_with_prefix()
    test_plot_contour()
    test_read_dicom_files()
    test_get_contour_data()
    # test_get_radiation_maps() - not working, need to fix


def playground():
    RS_file_path = find_file_with_prefix(EXAMPLE_FOLDER_Radiation_Plans, 'RS')
    RD_file_path = find_file_with_prefix(EXAMPLE_FOLDER_Radiation_Plans, 'RD')

    RS_data = read_dicom_rs_file(RS_file_path)
    RD_data = read_dicom_rd_file(RD_file_path)

    contour_data = get_contour_data(RS_data)

    # plot_contour(RS_data)

    # get_radiation_maps(RS_data)

    CT_file_path = find_file_with_prefix(EXAMPLE_FOLDER_CT, 'CT')
    CT_data = read_dicom_CT_file(CT_file_path)


def main():
    test_read_dicom_files()


main()
