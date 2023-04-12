import os
import subprocess
import sys
from P035_customer_files.preregister_tools.preregister import preregister


def main(hardware_version, order_number, model_number, first_serial_number, first_mac, last_mac, lot_size):
    create_mac_db_file = subprocess.run(["powershell",
                                         "-ExecutionPolicy",
                                         "Bypass",
                                         "C:\\softest_public_py\\P035\\P035_customer_files\\preregister_tools\\generate_mac.ps1",
                                         hardware_version,
                                         order_number,
                                         model_number,
                                         first_serial_number,
                                         first_mac,
                                         last_mac])
    print(create_mac_db_file.returncode, create_mac_db_file.stderr)

    with open("C:\\softest_public_py\\P035\\P035_customer_files\\preregister_tools\\production_environ.ps1", mode="r")\
            as environ_variables_file:
        environ_variables_texts = environ_variables_file.readlines()
    for environ_variable_text in environ_variables_texts:
        variable_name = environ_variable_text[5: environ_variable_text.find("=\"")]
        variable_value_temp = environ_variable_text[environ_variable_text.find("=\"") + 2:]
        variable_value = variable_value_temp[: variable_value_temp.find("\"")]
        os.environ.setdefault(variable_name, variable_value)
    os.environ.setdefault("TKE_LOT_SIZE", lot_size)
    for key in os.environ.keys():
        print(key, os.environ.get(key))

    # preregister()


if __name__ == '__main__':
    # will not work from here, script shall be triggered from labview vi or labview exe file
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
