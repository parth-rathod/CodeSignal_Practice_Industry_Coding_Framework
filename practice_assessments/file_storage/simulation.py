from dataclasses import dataclass
from datetime import datetime, timedelta

GIVEN_TIME_STAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"


@dataclass
class Container:
    filename: str
    filesize: str
    start_timestamp: datetime | None = None
    ttl: int | None = None

    @property
    def is_active_infinite(self):
        return True if self.ttl is None else False

    @property
    def end_timestamp(self) -> datetime | None:
        if self.start_timestamp and self.ttl:
            return self.start_timestamp + timedelta(seconds=self.ttl)
        return None


class RemoteServer:
    def __init__(self):
        self.container: list[Container] = []

    def file_upload(
        self,
        file_name: str,
        file_size: str,
        time_stamp: datetime | None = None,
        ttl: int | None = None,
    ) -> str | RuntimeError:
        if file_name in self.container:
            raise RuntimeError(f"File {file_name} already exists")
        else:
            self.container.append(
                Container(
                    filename=file_name,
                    filesize=file_size,
                    start_timestamp=time_stamp,
                    ttl=ttl,
                )
            )
        return f"uploaded {file_name}"

    def file_get(
        self, file_name: str, time_stamp: datetime | None = None
    ) -> str | None:
        for container in self.container:
            if container.filename == file_name:
                if container.is_active_infinite:
                    return container.filesize
                else:
                    if container.end_timestamp > time_stamp:
                        return container.filesize
        return None

    def file_copy(
        self,
        source_file_name: str,
        new_file_name: str,
        time_stamp: datetime | None = None,
    ) -> str | RuntimeError:
        for container in self.container:
            if container.filename == source_file_name:
                self.container.append(
                    Container(
                        filename=new_file_name,
                        filesize=container.filesize,
                        start_timestamp=time_stamp,
                    )
                )
                return f"copied {source_file_name} to {new_file_name}"
        raise RuntimeError(f"Source File {source_file_name} does not exists")

    def file_search(self, prefix: str, time_stamp: datetime | None = None) -> list[str]:
        temp_output = []
        for container in self.container:
            if container.filename.startswith(prefix):
                if container.is_active_infinite:
                    temp_output.append((container.filename, container.filesize))
                else:
                    if container.end_timestamp > time_stamp:
                        temp_output.append((container.filename, container.filesize))

        final_output = sorted(
            temp_output, key=lambda x: (-int(x[1].replace("kb", "")), x[0])
        )
        files = [f[0] for f in final_output]
        return files[:10]

    def file_upload_at(
        self,
        given_time_stamp: datetime,
        file_name: str,
        file_size: str,
        ttl: int | None = None,
    ) -> str | RuntimeError:
        time_stamp = datetime.strptime(given_time_stamp, GIVEN_TIME_STAMP_FORMAT)
        return self.file_upload(
            file_name=file_name, file_size=file_size, time_stamp=time_stamp, ttl=ttl
        )

    def file_get_at(self, given_time_stamp: datetime, file_name: str) -> str | None:
        time_stamp = datetime.strptime(given_time_stamp, GIVEN_TIME_STAMP_FORMAT)
        return self.file_get(file_name, time_stamp=time_stamp)

    def file_copy_at(
        self, given_time_stamp: datetime, source_file: str, destination_file: str
    ) -> str | RuntimeError:
        time_stamp = datetime.strptime(given_time_stamp, GIVEN_TIME_STAMP_FORMAT)
        return self.file_copy(
            source_file_name=source_file,
            new_file_name=destination_file,
            time_stamp=time_stamp,
        )

    def file_search_at(self, given_time_stamp: datetime, prefix: str) -> list[str]:
        time_stamp = datetime.strptime(given_time_stamp, GIVEN_TIME_STAMP_FORMAT)
        return self.file_search(prefix=prefix, time_stamp=time_stamp)

    def rollback(self, given_time_stamp: datetime) -> str:
        time_stamp = datetime.strptime(given_time_stamp, GIVEN_TIME_STAMP_FORMAT)
        removed_files = []
        for container in self.container:
            if container.start_timestamp and container.start_timestamp > time_stamp:
                removed_files.append(container)
        self.container = [c for c in self.container if c not in removed_files]
        return f"rollback to {given_time_stamp}"


def simulate_coding_framework(list_of_lists):
    """
    Simulates a coding framework operation on a list of lists of strings.

    Parameters:
    list_of_lists (List[List[str]]): A list of lists containing strings.
    """
    output = []
    remote_server = RemoteServer()
    for item in list_of_lists:
        command, *args = item
        if command == "FILE_UPLOAD":
            output.append(remote_server.file_upload(*args))
        elif command == "FILE_GET":
            output.append(remote_server.file_get(*args))
        elif command == "FILE_COPY":
            output.append(remote_server.file_copy(*args))
        elif command == "FILE_SEARCH":
            output.append(remote_server.file_search(*args))
        elif command == "FILE_UPLOAD_AT":
            output.append(remote_server.file_upload_at(*args))
        elif command == "FILE_GET_AT":
            output.append(remote_server.file_get_at(*args))
        elif command == "FILE_COPY_AT":
            output.append(remote_server.file_copy_at(*args))
        elif command == "FILE_SEARCH_AT":
            output.append(remote_server.file_search_at(*args))
        elif command == "ROLLBACK":
            output.append(remote_server.rollback(*args))
    return output


test_data_1 = [
    ["FILE_UPLOAD", "Cars.txt", "200kb"],
    ["FILE_GET", "Cars.txt"],
    ["FILE_COPY", "Cars.txt", "Cars2.txt"],
    ["FILE_GET", "Cars2.txt"],
]

test_data_2 = [
    ["FILE_UPLOAD", "Foo.txt", "100kb"],
    ["FILE_UPLOAD", "Bar.csv", "200kb"],
    ["FILE_UPLOAD", "Baz.pdf", "300kb"],
    ["FILE_UPLOAD", "Baa.pdf", "300kb"],
    ["FILE_SEARCH", "Ba"],
]

test_data_3 = [
    ["FILE_UPLOAD_AT", "2021-07-01T12:00:00", "Python.txt", "150kb"],
    ["FILE_UPLOAD_AT", "2021-07-01T12:00:00", "CodeSignal.txt", "150kb", 3600],
    ["FILE_GET_AT", "2021-07-01T13:00:01", "Python.txt"],
    ["FILE_COPY_AT", "2021-07-01T12:00:00", "Python.txt", "PythonCopy.txt"],
    ["FILE_SEARCH_AT", "2021-07-01T12:00:00", "Py"],
    ["FILE_UPLOAD_AT", "2021-07-01T12:00:00", "Expired.txt", "100kb", 1],
    ["FILE_GET_AT", "2021-07-01T12:00:02", "Expired.txt"],
    [
        "FILE_COPY_AT",
        "2021-07-01T12:00:00",
        "CodeSignal.txt",
        "CodeSignalCopy.txt",
    ],
    ["FILE_SEARCH_AT", "2021-07-01T12:00:00", "Code"],
]

test_data_4 = [
    ["FILE_UPLOAD_AT", "2021-07-01T12:00:00", "Initial.txt", "100kb"],
    ["FILE_UPLOAD_AT", "2021-07-01T12:05:00", "Update1.txt", "150kb", 3600],
    ["FILE_GET_AT", "2021-07-01T12:10:00", "Initial.txt"],
    ["FILE_COPY_AT", "2021-07-01T12:15:00", "Update1.txt", "Update1Copy.txt"],
    ["FILE_UPLOAD_AT", "2021-07-01T12:20:00", "Update2.txt", "200kb", 1800],
    ["ROLLBACK", "2021-07-01T12:10:00"],
    ["FILE_GET_AT", "2021-07-01T12:25:00", "Update1.txt"],
    ["FILE_GET_AT", "2021-07-01T12:25:00", "Initial.txt"],
    ["FILE_SEARCH_AT", "2021-07-01T12:25:00", "Up"],
    ["FILE_GET_AT", "2021-07-01T12:25:00", "Update2.txt"],
]


final_test_data = test_data_1 + test_data_2 + test_data_3 + test_data_4

if __name__ == "__main__":
    output = simulate_coding_framework(test_data_4)
    print(output)
