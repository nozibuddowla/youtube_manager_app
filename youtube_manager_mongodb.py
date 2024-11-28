from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()

db_uri = os.getenv("DB_URI")

client = MongoClient(db_uri)
db = client['ytmanager']
video_collection = db['videos']

def get_next_serial_number():
    last_video = video_collection.find_one(sort=[('serial_no', -1)])
    if last_video:
        return last_video['serial_no'] + 1
    else:
        return 1

def add_video(name, time):
    serial_no = get_next_serial_number()
    video_collection.insert_one({'serial_no': serial_no, 'name': name, 'time': time})
    print(f'Video "{name}" added with Serial No: {serial_no}')

def list_videos():
    print(f"\n{'Serial No.':<10}{'Name':<50}{'Time':<20}")
    print("-" * 80)
    for video in video_collection.find().sort("serial_no"):
        print(f"{video['serial_no']:<10}{video['name']:<50}{video['time']:<20}")

def update_video(serial_no, new_name, new_time):
    try:
        serial_no = int(serial_no)
        result = video_collection.update_one({'serial_no': serial_no}, {'$set': {'name': new_name, 'time': new_time}})
        if result.matched_count > 0:
            print(f"Video with Serial No: {serial_no} updated.")
        else:
            print(f"No video found with Serial No: {serial_no}")
    except ValueError:
        print("Invalid Serial No. Please enter a valid integer.")

def delete_video(serial_no):
    
    try:
        serial_no = int(serial_no)
        result = video_collection.delete_one({'serial_no': serial_no})
        if result.deleted_count > 0:
            print(f"Video with Serial No: {serial_no} deleted.")
        else:
            print(f"No video found with Serial No: {serial_no}")
    except ValueError:
        print("Invalid Serial No. Please enter a valid integer.")


def main():
    while True:
        print('\n YouTube Manager App')
        print('1. List all videos')
        print('2. Add a new video')
        print('3. Update a video')
        print('4. Delete a video')
        print('5. Exit')
        choice = input('Enter your choice: ')

        if choice == '1':
            list_videos()
        elif choice == '2':
            name = input('Enter the video title: ')
            time = input('Enter the video time Duration: ')
            add_video(name, time)
        elif choice == '3':
            list_videos()
            serial_no = input('Enter the serial number of the video to update: ')
            new_name = input('Enter the updated video title: ')
            new_time = input('Enter the updated video time Duration: ')
            update_video(serial_no, new_name, new_time)
        elif choice == '4':
            list_videos()
            serial_no = input('Enter the serial number of the video to delete: ')
            delete_video(serial_no)
        elif choice == '5':
            break
        else:
            print('Invalid choice!')

if __name__ == '__main__':
    main()