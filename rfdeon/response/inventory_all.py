class InventoryAll:
    def __init__(self, data: bytes):
        self.data = data

    @property
    def tags(self) -> list:
        length_tags = self.data[0]
        tags = []
        pointer = 1
        for _ in range(length_tags):
            len_tags = int(self.data[pointer])
            tag_data_start = pointer + 1
            tag_main_start = tag_data_start
            tag_main_end = tag_main_start + len_tags
            next_tag_start = tag_main_end
            tags.append(self.data[tag_main_start:tag_main_end])
            pointer = next_tag_start
        return tags


