from flask import Flask, json, request, Response
import base64

api = Flask(__name__)


@api.route('/alphadigi/lpr', methods=['GET', 'POST'])
def receiveData():
    plateResult = getPlateResultFromRequest()

    if not plateResult:
        error = 'Estrutura recebida é inválida'
        print(error)
        return error, 400

    content = request.json
    # print(content)
    save_image_from_request(request)
    return 'Dados recebidos'


def save_image_from_request(request):
    plateResult = request.json['AlarmInfoPlate']['result']['PlateResult']

    if not plateResult:
        return

    imageData = plateResult['imageFile']
    licensePlate = plateResult['license']

    print(licensePlate)

    decodedImageData = base64.b64decode(imageData)
    imagePath = 'output/' + licensePlate + '.jpg'
    with open(imagePath, 'wb') as imagePath:
        imagePath.write(decodedImageData)


def validateRequestAndGetPlateResult(request):
    plateResult = request.json['AlarmInfoPlate']['result']['PlateResult']

    if not plateResult:
        print('Requisição inválida')
        return False

    return plateResult


if __name__ == '__main__':
    api.run(host='0.0.0.0')
