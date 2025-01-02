import xml.etree.ElementTree as ET
import csv
import sys

def convert_xml_to_csv(xml_file, output_csv):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Open a CSV file for writing
    with open(output_csv, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        # Write the header row
        csvwriter.writerow(['Layer', 'Name', 'Verdict', 'Date', 'TestEquipment'])
        
        # Iterate through each TestCase and write the data to the CSV file
        for testcase in root.find('TestCases').findall('TestCase'):
            layer = testcase.find('Layer').text
            name = testcase.find('Name').text
            verdict = testcase.find('Verdict').text
            date = testcase.find('Date').text
            test_equipment = testcase.find('TestEquipment').text
            
            csvwriter.writerow([layer, name, verdict, date, test_equipment])

    print(f"XML data has been successfully converted to CSV file '{output_csv}'.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <xml_file> <output_csv>")
    else:
        xml_file = sys.argv[1]
        output_csv = sys.argv[2]
        convert_xml_to_csv(xml_file, output_csv)
