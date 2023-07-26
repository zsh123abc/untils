import json
import os
from PIL import Image



def generate_labelme_annotation(image_id, category_id, file_name, bbox, score, image_width, image_height):
    annotation = {
        "version": "5.2.0.post4",
        "flags": {},
        "shapes": [
            {
                "label": str(category_id),
                "points": [
                    [bbox[0], bbox[1]],
                    [bbox[2], bbox[1]],
                    [bbox[2], bbox[3]],
                    [bbox[0], bbox[3]]
                ],
                "group_id": None,
                "shape_type": "rectangle",
                "flags": {}
            }
        ],
        "imagePath": file_name,
        "imageData": None,
        "imageHeight": image_height,
        "imageWidth": image_width
    }

    return annotation

if __name__ == "__main__":
    # data = [
    #     {"image_id": 0, "category_id": 0, "file_name": "7_3_court1_0115.jpg", "bbox": [-5.720649719238281, 41.97674560546875, 1086.1176223754883, 1895.7910766601562], "score": 0.13662832975387573},
    #     # 添加更多数据...
    # ]

    with open(r"D:\zsh\bbox.json", "r") as f:
        data = json.load(f)

    output_dir = "annotations"
    os.makedirs(output_dir, exist_ok=True)

    for item in data:
        image_id = item["image_id"]
        category_id = item["category_id"]
        file_name = item["file_name"]
        bbox = item["bbox"]
        score = item["score"]
        img_file_name = file_name[:-4]+'.jpg'
        img_path = r'D:\zsh\7.7_court\part1\basketball_fram\img'
        img_file_name = img_path+'/'+img_file_name
        image = Image.open(img_file_name)
        image_width, image_height = image.size

        annotation = generate_labelme_annotation(image_id, category_id, file_name, bbox, score, image_width, image_height)
        output_dir = r'D:\zsh\7.7_court\part1\basketball_fram\json'
        output_file = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}.json")
        
        with open(output_file, "w") as f:
            json.dump(annotation, f)
        
        print(f"Generated labelme annotation for {file_name}.")

    print("All labelme annotations generated.")
