import fitz
import io
from PIL import Image
from unstructured.partition.pdf import partition_pdf


def get_text(file_path):
    text = ''
    try:
        blocks = partition_pdf(filename=file_path)
        text = [str(el) for el in blocks]
    except ImportError:
        print('Missing required dependencies')
    except Exception as e:
        print(f'Error encountered while loading file: {e}')
    
    return text


def get_images(file_path):
    doc = fitz.open(file_path)
    images_dict = {}
    for page_index in range(len(doc)):
        page = doc.load_page(page_index)
        image_li = page.get_images(full=True)
        for img_idx, img_info in enumerate(image_li):
            # image id
            xref = img_info[0]

            # get base img using id
            img = doc.extract_image(xref)
            img_bytes = img['image']
            img_ext = img['ext']

            try:
                image = Image.open(io.BytesIO(img_bytes))
                image_filename = f"{file_path}page{page_index+1}_img{img_idx+1}.{img_ext}"
                images_dict[image_filename] = image
            except Exception as e:
                print(f'could not load image. warning {e}')
    
    return images_dict


def extract_text_and_image(file_path):
    text = get_text(file_path)
    images = get_images(file_path)
    return {'text': text, 'images': images}
    

info = extract_text_and_image('data/res_1.pdf')