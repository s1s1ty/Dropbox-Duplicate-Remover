import dropbox
import asyncio

access_token = input("Your Dropbox Access Token?: ")

dbx = dropbox.Dropbox(access_token)
dbx.users_get_current_account()

file_stas = {}
duplicate = False


def folder_traverse(path):
    """Traverse all folder and find duplicate file
    @param: p is starting point
    @type: string
    """
    resp = dbx.files_list_folder(path=path)
    for i in resp.entries:
        if isinstance(i, dropbox.files.FolderMetadata):
            print("Checking....", i.name)
            folder_traverse(i.path_display)
        else:
            try:
                global duplicate
                duplicate = True
                file_stas[i.name][0] += 1
                file_stas[i.name][1].append(i.path_display)
            except:
                file_stas[i.name] = [1, [i.path_display]]


def show():
    print("\n--------------Total Duplicate File Found--------------\n")
    for k, v in file_stas.items():
        if v[0] > 1:
            print(k, "=", v)


async def delete(paths):
    """Delete file from the @param paths"""
    for path in paths:
        dbx.files_delete(path)


def main():
    folder_traverse("")
    show()
    if duplicate:
        want_delete = input("\n\nDo you want to delete duplicates? y/n: ")
        loop = asyncio.get_event_loop()
        if want_delete == 'y':
            for k, v in file_stas.items():
                if v[0] > 1:
                    print("Deleting....", k)
                    loop.run_until_complete(delete(v[1][1:]))
            loop.close()
    else:
        print("No duplicates found.")
    print("Thanks")


if __name__ == '__main__':
    main()
