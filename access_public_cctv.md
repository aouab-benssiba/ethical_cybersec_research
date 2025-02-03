# In this section we are going to cover: how to access public cctv security cameras.

- most of cctv ip cameras are indexed in a lot of search engine databases, and almost anyone can access without even loggin in.
- you can as well find default setup cctv using default creds to enter the stream
- here are some tipps to get started.

## First: search keywords

- inurl:Camera/index.html
- inurl:/view.shtml
- intitle:"Live View / - AXIS"
- inurl:axis-cgi/mjpg
- inurl:view/view.shtml
- inurl:view/index.shtml
- inurl:view/indexFrame.shtml
- inurl:view/viewer.shtml
- inurl:Camera/index.html
- inurl:live/index.html
- inurl:live/index.shtml
  
## Second: shodan or Censys  search engine keywords

- port:554 (RTSP stream port)

- port:80 (HTTP port for camera web interfaces)

- port:8080 (Alternative HTTP port)

- "Hikvision" (Search for specific brands)

- "Dahua" or "hikvision" or "D-link" (Search for specific brands)

- "RTSP" (Search for RTSP streams)
  
## Third: Exploit Default Credentials

Many IP cameras and IPTV devices use default usernames and passwords.
Common Default Credentials:

- Username: admin | Password: admin

- Username: admin | Password: 1234

- Username: admin | Password: password

- Username: root | Password: root

[more default creds](https://ipvm.com/reports/ip-cameras-default-passwords-directory)

## Forth: access the camera stream
i recommend to use VLC.

- RTSP URL Format:

- rtsp://<IP_ADDRESS>:554/stream

- rtsp://<IP_ADDRESS>:554/h264

- rtsp://<IP_ADDRESS>:554/mpeg4

## CCTV captures:

<details>
  <summary>Here some public cctv captures</summary>
  
![Screenshot 2025-02-03 194003](https://github.com/user-attachments/assets/14ca70e5-91ac-4ea6-a71b-7bd48947494c)
![Screenshot 2025-02-03 193801](https://github.com/user-attachments/assets/f1420cba-7f53-42ec-b41a-9330874f4262)
![Screenshot 2025-02-03 193743](https://github.com/user-attachments/assets/e3e6fe03-85a5-433e-9b14-e0d797e5e5c7)
![Screenshot 2025-02-03 193725](https://github.com/user-attachments/assets/157cb015-1c63-468c-a310-ef21bf374d44)
![Screenshot 2025-02-03 193625](https://github.com/user-attachments/assets/9fe07379-5743-46f5-960f-dcbf89361123)
![Screenshot 2025-02-03 192745](https://github.com/user-attachments/assets/040d26c4-b1d8-4b1f-b4a0-fd367468df75)
![Screenshot 2025-02-03 192711](https://github.com/user-attachments/assets/071d5217-7b96-406b-a3a0-2020cd7fb419)
![Screenshot 2025-02-03 194236](https://github.com/user-attachments/assets/970d171d-44f8-445f-a971-0d263af8b234)
![Screenshot 2025-02-03 194108](https://github.com/user-attachments/assets/2acb31d5-bfda-4b41-b8b9-d3fdf6ada53d)

</details>

