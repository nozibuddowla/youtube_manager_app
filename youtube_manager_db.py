import sqlite3

con = sqlite3.connect('youtube_videos.db')

cur = con.cursor()

cur.execute(""" 
    CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                time TEXT NOT NULL
    )
""")

def list_all_videos():
    cur.execute('SELECT * FROM videos')
    videos = cur.fetchall()

    if not videos:
        print("No videos found.")
        return

    print(f"\n{'ID':<5} {'Title':<60} {'Duration':<20}")
    print("-" * 85)
    for row in videos:
        title = row[1] if len(row[1]) <= 57 else row[1][:57] + "..."
        print(f"{row[0]:<5} {title:<60} {row[2]:<20}")


def add_video(name, time):
    cur.execute('INSERT INTO videos (name, time) VALUES (?, ?)', (name, time))
    con.commit()

def update_video(video_id, new_name, new_time):
    cur.execute('UPDATE videos SET name = ?, time = ? WHERE id = ?', (new_name, new_time, video_id))
    con.commit()

def delete_video(video_id):
    cur.execute('DELETE FROM videos where id = ?', (video_id,))
    con.commit()

def main():
    while True:
        print('\n YouTube Manager app with DB | choose an option: ')
        print('1. List all youtube videos')
        print('2. Add a youtube video')
        print('3. Update a youtube video details')
        print('4. Delete a youtube video')
        print('5. Exit the app')
        choice = input('Enter your choice: ')

        if choice == '1':
            list_all_videos()
        elif choice == '2':
            name = input('Enter your video name: ')
            time = input('Enter your video time: ')
            add_video(name, time)
            list_all_videos()
        elif choice == '3':
            list_all_videos()
            video_id = input('Enter video ID to update: ')
            new_name = input('Enter your video name: ')
            new_time = input('Enter your video time: ')
            update_video(video_id, new_name, new_time)
        elif choice == '4':
            list_all_videos()
            video_id = input('Enter video ID to delete: ')
            delete_video(video_id)
        elif choice == '5':
            break
        else:
            print('Invalid choice')

    con.close()

if __name__ == '__main__':
    main()
