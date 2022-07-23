import cv2
import io
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import FormRecognizerClient

import os
import time

from modules.keys import keys
import modules.speech as speech

engine = speech.Speech()

'''
Describe an Image
'''


def describeScene(cam):
    ret, frame = cam.read()
    if ret == None:
        engine.text_to_speech("Not getting any frame. Quitting now...")
    else:
        cv2.imwrite('op.jpg', frame)
        print("===== Describe an Image =====")
        # images_folder = os.path.join (os.path.dirname(os.path.abspath(__file__)), "images")
        path = 'op.jpg'
        # Open local image file
        # local_image_path = os.path.join (images_folder, "")
        local_image = open(path, "rb")

        # <snippet_client>
        computervision_client = ComputerVisionClient(
            keys['vision_endpoint'], CognitiveServicesCredentials(keys['vision_key']))
        # </snippet_client>

        # Call API
        description_result = computervision_client.describe_image_in_stream(
            local_image)

        # Get the captions (descriptions) from the response, with confidence level
        print("Description of the view: ")
        engine.text_to_speech("Description of the view: ")
        if (len(description_result.captions) == 0):
            engine.text_to_speech("No description detected")
        else:
            for caption in description_result.captions:
                print("'{}' with confidence {:.2f}%".format(
                    caption.text, caption.confidence * 100))
                engine.text_to_speech(caption.text)
        print()
        '''
        END - Describe an Image
        '''
        categorizeObjects(path)
        detectObjects(path)


def categorizeObjects(path):
    '''
    Categorize an Image
    '''
    print("===== Categorize an Image - local =====")
    # # Open local image file
    local_image = open(path, "rb")

    # local_image = open(path, "rb")
    # Select visual feature type(s)
    local_image_features = ["categories"]

    # <snippet_client>
    computervision_client = ComputerVisionClient(
        keys['vision_endpoint'], CognitiveServicesCredentials(keys['vision_key']))
    # </snippet_client>

    # Call API
    categorize_results_local = computervision_client.analyze_image_in_stream(
        local_image, local_image_features)

    # Print category results with confidence score
    print("Categories from image: ")
    engine.text_to_speech("I will categorize the objects around you")
    if (len(categorize_results_local.categories) == 0):
        engine.text_to_speech("No categories detected")
    else:
        for category in categorize_results_local.categories:
            name = category.name.split("_")
            name = ' '.join(name)
            print("'{}' with confidence {:.2f}%".format(
                category.name, category.score * 100))
            engine.text_to_speech(name)
    print()
    '''
    END - Categorize an Image
    '''


def detectObjects(path):
    '''
    Detect Objects - local
    This example detects different kinds of objects with bounding boxes in a local image.
    '''
    print("===== Detect Objects =====")

    # Get  image with different objects in it
    # local_image_path_objects = os.path.join (images_folder, "face3.jpeg")
    # local_image_objects = open(local_image_path_objects, "rb")
    # Call API with local image
    engine.text_to_speech("Now, I will tell you the objects near you.")
    local_image = open(path, "rb")

    # <snippet_client>
    computervision_client = ComputerVisionClient(
        keys['vision_endpoint'], CognitiveServicesCredentials(keys['vision_key']))
    # </snippet_client>

    detect_objects_results_local = computervision_client.detect_objects_in_stream(
        local_image)

    # Print results of detection with bounding boxes
    print("Detecting objects in image:")
    if len(detect_objects_results_local.objects) == 0:
        engine.text_to_speech("No objects detected")
    else:
        for object in detect_objects_results_local.objects:
            print(object.object_property)
            engine.text_to_speech(object.object_property)
    print()
    '''
    END - Detect Objects
    '''
    checkRoad(detect_objects_results_local.objects)


def checkRoad(labels):
    road = 0
    car = 0
    motor_vehicle = 0
    bicycle = 0
    classroom = 0
    truck = 0
    traffic = 0
    face = 0
    for i, label in enumerate(labels):
        label = label.object_property.lower()
        if (label == "highway" or label == "lane" or label == "road"):
            road += 1
        if (label == "car"):
            car += 1
        if (label == "motor vehicle"):
            motor_vehicle += 1
        if (label == "bicycle"):
            bicycle += 1
        if (label == "truck"):
            truck += 1
        if (label == "face"):
            face += 1
        if (label == "classroom"):
            classroom += 1
        if (label == "traffic"):
            traffic += 1

    road = False
    if car > 0 or motor_vehicle > 0 or truck > 0 or bicycle > 0 or traffic > 0:
        road = True

    if (road):
        if (car >= 2 or motor_vehicle >= 1 or bicycle >= 3 or truck >= 1 or traffic >= 1):
            engine.text_to_speech(
                "It seems you are walking on a road with vehicles. Beware!")
            road = True
        else:
            engine.text_to_speech(
                "It seems the road you are walking on is quite safe. Yet beware.")
    if (classroom >= 1):
        engine.text_to_speech("You seem to be in a classroom!")


def read(cam):
    '''
    OCR: Read File using the Read API, extract text - local
    This example extracts text from a local image, then prints results.
    This API call can also recognize remote image text (shown in next example, Read File - remote).
    '''
    ret, frame = cam.read()
    if ret == None:
        engine.text_to_speech("Not getting any frame. Quitting now...")
    else:
        cv2.imwrite('op.jpg', frame)
    print("===== Read File =====")
    engine.text_to_speech("Reading the intended text")

    # Get image path
    # images_folder = os.path.join (os.path.dirname(os.path.abspath(__file__)), "images")
    # read_image_path = os.path.join (images_folder, "french.jpeg")
    # Open the image
    path = "op.jpg"
    read_image = open(path, "rb")

    # <snippet_client>
    computervision_client = ComputerVisionClient(
        keys['vision_endpoint'], CognitiveServicesCredentials(keys['vision_key']))
    # </snippet_client>

    # Call API with image and raw response (allows you to get the operation location)
    read_response = computervision_client.read_in_stream(read_image, raw=True)
    # Get the operation location (URL with ID as last appendage)
    read_operation_location = read_response.headers["Operation-Location"]
    # Take the ID off and use to get results
    operation_id = read_operation_location.split("/")[-1]

    # Call the "GET" API and wait for the retrieval of the results
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status.lower() not in ['notstarted', 'running']:
            break
        engine.text_to_speech("Waiting for result...")
        time.sleep(10)

    # Print results, line by line
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                print(line.text)
                engine.text_to_speech(line.text)
                print(line.bounding_box)
    print()


def color(cam):
    ret, frame = cam.read()
    if ret == None:
        engine.text_to_speech("Not getting any frame. Quitting now...")
    else:
        cv2.imwrite('op.jpg', frame)
        path = "op.jpg"
        print("===== Detect Color =====")
        engine.text_to_speech("Detecting dominant colors of the frame")
        # Open local image
        local_image = open(path, "rb")
        # Select visual feature(s) you want
        local_image_features = ["color"]

        # <snippet_client>
        computervision_client = ComputerVisionClient(
            keys['vision_endpoint'], CognitiveServicesCredentials(keys['vision_key']))
        # </snippet_client>

        # Call API with local image and features
        detect_color_results_local = computervision_client.analyze_image_in_stream(
            local_image, local_image_features)

        # Print results of the color scheme detected
        engine.text_to_speech("Getting color scheme of the frame: ")

        engine.text_to_speech("Is black and white: {}".format(
            detect_color_results_local.color.is_bw_img))

        engine.text_to_speech("Accent color: {}".format(
            detect_color_results_local.color.accent_color))

        engine.text_to_speech("Dominant background color: {}".format(
            detect_color_results_local.color.dominant_color_background))

        engine.text_to_speech("Dominant foreground color: {}".format(
            detect_color_results_local.color.dominant_color_foreground))

        engine.text_to_speech("Dominant colors: {}".format(
            detect_color_results_local.color.dominant_colors))

        print()


def analyzeReceipt():

    path_to_sample_forms = os.path.abspath(
        os.path.join(
            os.path.abspath(__file__),
            "..",
            "..",
            "./images/ReceiptSwiss.jpg",
        )
    )

    endpoint = "https://drishti-form-recognizer.cognitiveservices.azure.com/"
    key = "1de10cfec68840f8836c6e4cf9fa87db"

    form_recognizer_client = FormRecognizerClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    with open(path_to_sample_forms, "rb") as f:
        poller = form_recognizer_client.begin_recognize_receipts(
            receipt=f, locale="en-US")
    receipts = poller.result()

    for idx, receipt in enumerate(receipts):
        print("--------Recognizing receipt #{}--------".format(idx+1))
        engine.text_to_speech("Recognizing receipt")
        receipt_type = receipt.fields.get("ReceiptType")
        if receipt_type:
            print("Receipt Type: {} has confidence: {}".format(
                receipt_type.value, receipt_type.confidence))
            engine.text_to_speech(
                "Receipt Type: {}".format(receipt_type.value))
        merchant_name = receipt.fields.get("MerchantName")
        if merchant_name:
            print("Merchant Name: {} has confidence: {}".format(
                merchant_name.value, merchant_name.confidence))
            engine.text_to_speech(
                "Merchant Name: {}".format(merchant_name.value))
        transaction_date = receipt.fields.get("TransactionDate")
        if transaction_date:
            print("Transaction Date: {} has confidence: {}".format(
                transaction_date.value, transaction_date.confidence))
            engine.text_to_speech(
                "Transaction Date: {}".format(transaction_date.value))

        if receipt.fields.get("Items"):
            print("Receipt items:")
            engine.text_to_speech("The following are the receipt items:")

            for idx, item in enumerate(receipt.fields.get("Items").value):
                print("...Item #{}".format(idx+1))
                engine.text_to_speech("Item Number {}".format(idx + 1))

                item_name = item.value.get("Name")
                if item_name:
                    print("......Item Name: {} has confidence: {}".format(
                        item_name.value, item_name.confidence))
                    engine.text_to_speech(
                        "Item name {}".format(item_name.value))

                item_quantity = item.value.get("Quantity")
                if item_quantity:
                    print("......Item Quantity: {} has confidence: {}".format(
                        item_quantity.value, item_quantity.confidence))
                    engine.text_to_speech(
                        "Item quantity {}".format(item_quantity.value))

                item_price = item.value.get("Price")
                if item_price:
                    print("......Individual Item Price: {} has confidence: {}".format(
                        item_price.value, item_price.confidence))
                    engine.text_to_speech(
                        "Individual item price {}".format(item_price.value))

                item_total_price = item.value.get("TotalPrice")
                if item_total_price:
                    print("......Total Item Price: {} has confidence: {}".format(
                        item_total_price.value, item_total_price.confidence))

                    engine.text_to_speech(
                        "Total item price {}".format(item_total_price.value))
        subtotal = receipt.fields.get("Subtotal")
        if subtotal:
            print("Subtotal: {} has confidence: {}".format(
                subtotal.value, subtotal.confidence))
            engine.text_to_speech("Subtotal {}".format(subtotal.value))

        tax = receipt.fields.get("Tax")
        if tax:
            print("Tax: {} has confidence: {}".format(
                tax.value, tax.confidence))
            engine.text_to_speech("Tax {}".format(tax.value))

        tip = receipt.fields.get("Tip")
        if tip:
            print("Tip: {} has confidence: {}".format(
                tip.value, tip.confidence))
            engine.text_to_speech("Tip {}".format(tip.value))
        total = receipt.fields.get("Total")
        if total:
            print("Total: {} has confidence: {}".format(
                total.value, total.confidence))
            engine.text_to_speech("Total {}".format(total.value))
        print("--------------------------------------")
