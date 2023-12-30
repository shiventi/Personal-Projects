import cv2
import face_recognition
import subprocess
import platform

def open_incognito_window(browser='chrome'):
    system = platform.system()
    browser_commands = {'chrome': {'Windows': 'start chrome --incognito', 'Darwin': 'open -a "Google Chrome" --args --incognito', 'Linux': 'google-chrome --incognito'}, 'brave': {'Windows': 'start brave --incognito', 'Darwin': 'open -a "Brave Browser" --args --incognito', 'Linux': 'brave-browser --incognito'}}
    browser_lower = browser.lower()


    if browser_lower not in browser_commands or system not in browser_commands[browser_lower]:
        print("nope not working")
        return

    subprocess.run(browser_commands[browser_lower][system], shell=True)

def open_in_incognito_tab(browser_name, url):
    applescript = f'''tell application "{browser_name}"\nif it is running then\nmake new tab at end of tabs of window 1 with properties {{URL:"{url}"}}\nelse\nopen location "{url}"\nend if\nactivate\nend tell\n'''
   
    subprocess.run(['osascript', '-e', applescript])

def run_website_opener():
    url = "https://"
    url_1 = url + 'example1'
    url_2 = url + 'example2'
    url_3 = url + 'example3'

    subprocess.run(['open', '-a', "app1"])
    subprocess.run(["open", "-a", "app2"])

    open_incognito_window("Chrome")
    open_in_incognito_tab("Google Chrome", url_1)
    open_in_incognito_tab("Google Chrome", url_2)

    open_incognito_window("Brave")

    open_in_incognito_tab("Brave Browser", url_3)

global true_false
true_false = False

def take_picture():
    try: 
        video_capture = cv2.VideoCapture(0)
        video_capture.set(3, 400)
        video_capture.set(4, 400)
        print(f"please look at camera!")
        ret, frame = video_capture.read()
        cv2.imwrite('faces/reference_image.jpg', frame)
        video_capture.release()
        cv2.destroyAllWindows()
    except:
        video_capture = cv2.VideoCapture(1)
        video_capture.set(3, 400)
        video_capture.set(4, 400)
        print(f"please look at camera!")
        ret, frame = video_capture.read()
        cv2.imwrite('faces/reference_image.jpg', frame)

        video_capture.release()

        cv2.destroyAllWindows()

def capture_reference_image():
    take_picture()

def compare_faces(key_image_path, test_image_path):
    key_image = face_recognition.load_image_file(key_image_path)

    key_face_encoding = face_recognition.face_encodings(key_image)[0]
    test_image = face_recognition.load_image_file(test_image_path)


    test_face_encoding = face_recognition.face_encodings(test_image)
    if not test_face_encoding:
        print("where is your face gone?")
        return False

    results = face_recognition.compare_faces([key_face_encoding], test_face_encoding[0])
    if results[0]:
        print("You are him!")
        global true_false
        true_false = True

        return True


    else:
        print("You are not him!")
        run_website_opener()
        return False

if __name__ == "__main__":
    capture_reference_image()
    key = "faces/key_image.jpg"
    check = "faces/reference_image.jpg"
    compare_faces(key, check)
    if true_false == False:
        pass
    else:
        run_website_opener()