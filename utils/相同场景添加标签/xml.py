import xml.etree.ElementTree as ET
import os
xml = r"D:\zsh\biaozhu\toulan63toulan4-shot0-miss1\xml"

# 相同场景，位置不变，为没有篮板，篮筐，篮网的xml标注添加对应数据

for xml_path in os.listdir(xml):
    xml_path = xml +'\\'+xml_path
    tree = ET.parse(xml_path)
    root = tree.getroot()

    import xml.etree.ElementTree as ET

    tree = ET.parse(xml_path)
    root = tree.getroot()

    for annotation in root.iter('annotation'):
        test = [obj.find('name').text for obj in annotation.findall('object')]
        if 'backboard' not in test:
            backboard = ET.SubElement(annotation, 'object')
            name = ET.SubElement(backboard, 'name')
            name.text = 'backboard'
            pose = ET.SubElement(backboard, 'pose')
            pose.text = 'Unspecified' 
            truncated = ET.SubElement(backboard, 'truncated')
            truncated.text = '0'
            difficult = ET.SubElement(backboard, 'difficult')
            difficult.text = '0'
            bndbox = ET.SubElement(backboard, 'bndbox')
            xmin = ET.SubElement(bndbox, 'xmin')
            xmin.text = '417'
            ymin = ET.SubElement(bndbox, 'ymin')
            ymin.text = '116'
            xmax = ET.SubElement(bndbox, 'xmax')
            xmax.text = '493'
            ymax = ET.SubElement(bndbox, 'ymax')
            ymax.text = '161'
        if 'basket_net' not in test:
            basket_net = ET.SubElement(annotation, 'object')
            name = ET.SubElement(basket_net, 'name')
            name.text = 'basket_net'
            pose = ET.SubElement(basket_net, 'pose')
            pose.text = 'Unspecified'
            truncated = ET.SubElement(basket_net, 'truncated')
            truncated.text = '0'
            difficult = ET.SubElement(basket_net, 'difficult')
            difficult.text = '0'
            bndbox = ET.SubElement(basket_net, 'bndbox')
            xmin = ET.SubElement(bndbox, 'xmin')
            xmin.text = '445'
            ymin = ET.SubElement(bndbox, 'ymin')
            ymin.text = '147'
            xmax = ET.SubElement(bndbox, 'xmax')
            xmax.text = '468'
            ymax = ET.SubElement(bndbox, 'ymax')
            ymax.text = '170'
        if 'basketball_frame' not in test:
            basketball_frame = ET.SubElement(annotation, 'object')
            name = ET.SubElement(basketball_frame, 'name')
            name.text = 'basketball_frame'
            pose = ET.SubElement(basketball_frame, 'pose')
            pose.text = 'Unspecified'
            truncated = ET.SubElement(basketball_frame,'truncated')
            truncated.text = '0'
            difficult = ET.SubElement(basketball_frame, 'difficult')
            difficult.text = '0'
            bndbox = ET.SubElement(basketball_frame, 'bndbox')
            xmin = ET.SubElement(bndbox, 'xmin')
            xmin.text = '444'
            ymin = ET.SubElement(bndbox, 'ymin')
            ymin.text = '147'
            xmax = ET.SubElement(bndbox, 'xmax')
            xmax.text = '466'
            ymax = ET.SubElement(bndbox, 'ymax')
            ymax.text = '153'
        
        ET.indent(root, space="\t", level=0)
        tree.write(xml_path, encoding="utf-8", xml_declaration=True)









