import dataclasses

HeaderName_t = str
HeaderValue_t = str
HeaderEntry_t = tuple[HeaderName_t, HeaderValue_t]

@dataclasses.dataclass
class Mail:
    headers: list[HeaderEntry_t]
    body: list[str]

