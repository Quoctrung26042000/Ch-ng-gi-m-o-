import cv2
import config
import process_database

path_save = 'get_image'

def get_image():
    process_database.connect_database()

    print("Please enter your id (MUST be an integer) to check your face ===>>>  ")
    take_face_id = input()


    name_img, name_user, img_id, face_id = process_database.getImg(pathSave = path_save, id = take_face_id)

    print(name_user)
    print(name_img)

    name_img_new = name_img.split(".")[0] + "." + str(take_face_id) + "." + name_img.split(".")[1] + "_" + str(img_id) +".jpg"

    img = cv2.imread(f'get_image/{name_img_new}')

    cv2.imshow(f'This face is: {name_user}', img)

    print("This face is: ", name_user)

    cv2.waitKey(0)
    process_database.disconnect_database()


if __name__ == '__main__':
    get_image()