"""
Services for working with API Google Drive
"""

from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from googleapiclient.discovery import build
import pprint
import io

pp = pprint.PrettyPrinter(indent=4)
# Set API Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'molten-reach-374314-ff8614f07f39.json'
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)


def get_file_id(file_name):
    """Getting file id"""
    file = gd_show_file(file_name)
    try:
        file_id = file[0]['id']
        return file_id
    except IndexError:
        return "There are no files there"


def gd_show_all_files():
    """Getting information about all the files at GD folder"""
    results = service.files().list(pageSize=10,
                                   fields="nextPageToken, files(id, name, mimeType)").execute()
    nextPageToken = results.get('nextPageToken')
    while nextPageToken:
        nextPage = service.files().list(pageSize=10,
                                        fields="nextPageToken, files(id, name, mimeType, parents)",
                                        pageToken=nextPageToken).execute()
        nextPageToken = nextPage.get('nextPageToken')
        results['files'] = results['files'] + nextPage['files']
    print(f"There are {len(results.get('files'))} files")
    return results


def gd_show_file(file_name):
    """Showing one file at GD folder"""
    results = service.files().list(
        pageSize=10,
        fields="nextPageToken, files(id, name, mimeType, parents, createdTime)",
        q=f"name = '{file_name}'").execute()
    return results['files']


def gd_download_file(file_name):
    """Download file from at GD folder"""
    file_id = get_file_id(file_name)
    request = service.files().get_media(fileId=file_id)
    filename = file_name
    fh = io.FileIO(filename, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    return ""


def gd_upload_file(file_name, file_dir):
    """Upload file to GD folder"""
    folder_id = '1ZJKicv243v9ekvUmPBxqmlJUct4pLtRJ'
    name = file_name
    file_path = file_dir
    file_metadata = {
        'name': name,
        'parents': [folder_id]
    }
    media = MediaFileUpload(fr'{file_path}', resumable=True)
    r = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    pp.pprint(r)


def gd_delete_file(file_name):
    """Delete file from GD folder"""
    file_id = get_file_id(file_name)
    service.files().delete(fileId=file_id).execute()
