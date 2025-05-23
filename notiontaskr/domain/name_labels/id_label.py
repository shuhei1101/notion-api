from dataclasses import dataclass

from notiontaskr.domain.name_labels.label_registerable import LabelRegisterable
from notiontaskr.domain.name_labels.name_label import NameLabel
from notiontaskr.domain.value_objects.notion_id import NotionId
from notiontaskr.domain.value_objects.status import Status


@dataclass
class IdLabel(NameLabel):

    @classmethod
    def from_property(cls, id: NotionId, status: Status) -> "IdLabel":
        """IDラベルを生成する"""
        if status == Status.NOT_STARTED:
            key = ""
        elif status == Status.COMPLETED:
            key = "✓"
        elif status == Status.IN_PROGRESS:
            key = "→"
        elif status == Status.DELAYED:
            key = "!"
        elif status == Status.CANCELED:
            key = "×"
        else:
            key = ""

        return cls(
            key=key,
            value=str(id.number),
        )

    @classmethod
    def parse_and_register(cls, key: str, value: str, delegate: "LabelRegisterable"):
        """ラベルを解析して登録する

        if文の順番に注意。"✓"は絵文字に含まれないため、最初に判定する。
        """
        label = key + value  # 一度文字列を結合する

        key_value_symbols = ["→", "!", "✓", "×"]

        if label[0].isdigit():
            key = ""
            value = label
        elif label[0] in key_value_symbols:
            key = label[0]
            value = label[1:]
        else:
            raise ValueError(f"Unknown key: {key}")

        delegate.register_id_label(
            cls(
                key=key,
                value=str(value),
            )
        )
