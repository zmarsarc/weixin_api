# coding=utf-8
import xml.etree.ElementTree as ElementTree


class base_message(object):

    """微信传递的 xml 数据包的基类"""

    def __init__(self, serialized_xml=None):
        super(base_message, self).__init__()

        self.__setup_filed()
        if serialized_xml is not None:
            self.__import_tree(serialized_xml)
        else:
            self.__create_empty_tree()

    def __import_tree(self, serialized_xml):
        self._xml = ElementTree.fromstring(serialized_xml)
        self._ToUserName = self._xml.find('ToUserName').text
        self._FromUserName = self._xml.find('FromUserName').text
        self._CreateTime = int(self._xml.find('CreateTime').text)
        self._MsgId = int(self._xml.find('MsgId').text)

    def __setup_filed(self):
        self._xml = None
        self._ToUserName = None
        self._FromUserName = None
        self._CreateTime = None
        self._MsgId = None

    @property
    def to_user_name(self):
        return self._ToUserName

    @to_user_name.setter
    def to_user_name(self, name):
        self._ToUserName = name
        self.__set_text('ToUserName', name)

    @property
    def from_user_name(self):
        return self._FromUserName

    @from_user_name.setter
    def from_user_name(self, name):
        self._FromUserName = name
        self.__set_text('FromUserName', name)

    @property
    def create_time(self):
        return self._CreateTime

    @create_time.setter
    def create_time(self, time):
        self._CreateTime = time
        self.__set_text('CreateTime', str(time))

    @property
    def msg_id(self):
        return self._MsgId

    @msg_id.setter
    def msg_id(self, package_id):
        self._MsgId = package_id
        self.__set_text('MsgId', str(package_id))

    def dump(self):
        msg_type = self._xml.find('MsgType')
        if msg_type is None:
            msg_type = ElementTree.SubElement(self._xml, 'MsgType')
        msg_type.text = str(self)
        return ElementTree.dump(self._xml)

    def __create_empty_tree(self):
        root = ElementTree.Element('xml')
        ElementTree.SubElement(root, 'ToUserName')
        ElementTree.SubElement(root, 'FromUserName')
        ElementTree.SubElement(root, 'CreateTime')
        ElementTree.SubElement(root, 'MsgId')
        self._xml = root

    def __set_text(self, section, text):
        self._xml.find(section).text = text

    def __str__(self):
        return 'base_message'


class text(base_message):

    def __init__(self, serialized_xml):
        super(text, self).__init__(serialized_xml)

        self.__setup_filed()
        if serialized_xml is not None:
            self.__import_tree(serialized_xml)
        else:
            self.__create_empty_tree()

    @property
    def content(self):
        return self._Content

    @content.setter
    def content(self, text):
        self._Content = text
        self.__set_text('Content', text)

    def __setup_filed(self):
        self._Content = None

    def __import_tree(self, serialized_xml):
        self._Content = self._xml.find('Content').text

    def __create_empty_tree(self):
        ElementTree.SubElement(self._xml, 'Content')

    def __str__(self):
        return 'text'


class media(base_message):

    def __init__(self, serialized_xml):
        super(media, self).__init__(serialized_xml)

        self.__setup_filed()
        if serialized_xml is not None:
            self.__import_tree(serialized_xml)
        else:
            self.__create_empty_tree()

    def __setup_filed(self):
        self._MediaId = None

    def __import_tree(self, serialized_xml):
        self._MediaId = self._xml.find('MediaId').text

    def __create_empty_tree(self):
        ElementTree.SubElement(self._xml, 'MediaId')

    @property
    def media_id(self):
        return self._MediaId

    @media_id.setter
    def media_id(self, id):
        self._MediaId = id
        self.__set_text('MediaId', id)

    def __str__(self):
        return 'media'


class image(media):

    def __init__(self, serialized_xml):
        super(image, self).__init__(serialized_xml)

        self.__setup_filed()
        if serialized_xml is not None:
            self.__import_tree(serialized_xml)
        else:
            self.__create_empty_tree()

    def __setup_filed(self):
        self._PicUrl = None

    def __import_tree(self, serialized_xml):
        self._PicUrl = self._xml.find('PicUrl').text

    def __create_empty_tree(self):
        ElementTree.SubElement(self._xml, 'PicUrl')

    @property
    def picture_url(self):
        return self._PicUrl

    @picture_url.setter
    def picture_url(self, url):
        self._PicUrl = url
        self.__set_text('PicUrl', url)

    def __str__(self):
        return 'image'


class voice(media):

    def __init__(self, serialized_xml):
        super(voice, self).__init__(serialized_xml)

        self.__setup_filed()
        if serialized_xml is not None:
            self.__import_tree(serialized_xml)
        else:
            self.__create_empty_tree()

    def __setup_filed(self):
        self._Format = None
        self._Recognition = None

    def __import_tree(self, serialized_xml):
        self._Format = self._xml.find('Format').text
        self._Recognition = self._xml.find('Recognition').text

    def __create_empty_tree(self):
        ElementTree.SubElement(self._xml, 'Format')
        ElementTree.SubElement(self._xml, 'Recognition')

    @property
    def format(self):
        return self._Format

    @format.setter
    def format(self, ft):
        self._Format = ft
        self.__set_text('Format', ft)

    @property
    def recognition(self):
        return self._Recognition

    @recognition.setter
    def recognition(self, re):
        self._Recognition = re
        self.__set_text('Recognition', re)

    def __str__(self):
        return 'voice'


class video(media):

    def __init__(self, serialized_xml):
        super(video, self).__init__(serialized_xml)

        self.__setup_filed()
        if serialized_xml is not None:
            self.__import_tree(serialized_xml)
        else:
            self.__create_empty_tree()

    def __setup_filed(self):
        self._ThumbMediaId = None

    def __import_tree(self, serialized_xml):
        self._ThumbMediaId = self._xml.find('ThumbMediaId').text

    def __create_empty_tree(self):
        ElementTree.SubElement(self._xml, 'ThumbMediaId')

    @property
    def thumb(self):
        return self._ThumbMediaId

    @thumb.setter
    def thumb(self, media_id):
        self._ThumbMediaId = media_id
        self.__set_text('ThumbMediaId', media_id)

        def __str__(self):
            return 'video'


class shortvideo(video):

    def __str__(self):
        return 'shortvideo'


class location(base_message):

    def __init__(self, serialized_xml):
        super(location, self).__init__(serialized_xml)

        self.__setup_filed()
        if serialized_xml is not None:
            self.__import_tree(serialized_xml)
        else:
            self.__create_empty_tree()

    def __setup_filed(self):
        self._Location_X = None
        self._Location_Y = None
        self._Scale = None
        self._Lable = None

    def __import_tree(self, serialized_xml):
        self._Location_X = float(self._xml.find('Location_X').text)
        self._Location_Y = float(self._xml.find('Location_Y').text)
        self._Scale = float(self._xml.find('Scale').text)
        self._Lable = self._xml.find('Label').text

    def __create_empty_tree(self):
        ElementTree.SubElement(self._xml, 'Location_X')
        ElementTree.SubElement(self._xml, 'Location_Y')
        ElementTree.SubElement(self._xml, 'Scale')
        ElementTree.SubElement(self._xml, 'Label')

    @property
    def location_x(self):
        return self._Location_X

    @location_x.setter
    def location_x(self, pos):
        self._Location_X = pos
        self.__set_text('Location_X', str(pos))

    @property
    def location_y(self):
        return self._Location_Y

    @location_y.setter
    def location_y(self, pos):
        self._Location_Y = pos
        self.__set_text('Location_Y', str(pos))

    @property
    def scale(self):
        return self._Scale

    @scale.setter
    def scale(self, scale):
        self._Scale = scale
        self.__set_text('Scale', str(scale))

    @property
    def label(self):
        return self._Lable

    @label.setter
    def label(self, text):
        self._Lable = text
        self.__set_text('Label', text)

    def __str__(self):
        return 'location'


class link(base_message):

    def __init__(self, serialized_xml=None):
        super(link, self).__init__()

        self.__setup_filed()
        if serialized_xml is not None:
            self.__import_tree(serialized_xml)
        else:
            self.__create_empty_tree()

    def __setup_filed(self):
        self._Title = None
        self._Description = None
        self._Url = None

    def __import_tree(self, serialized_xml):
        self._Title = self._xml.find('Title').text
        self._Description = self._xml.find('Description').text
        self._Url = self._xml.find('Url').text

    def __create_empty_tree(self):
        ElementTree.SubElement(self._xml, 'Title')
        ElementTree.SubElement(self._xml, 'Description')
        ElementTree.SubElement(self._xml, 'Url')

    @property
    def title(self):
        return  self._Title

    @title.setter
    def title(self, text):
        self._Title = text
        self.__set_text('Title', text)

    @property
    def description(self):
        return self._Description

    @description.setter
    def description(self, text):
        self._Description = text
        self.__set_text('Description', text)

    @property
    def url(self):
        return self._Url

    @url.setter
    def url(self, url):
        self._Url = url
        self.__set_text('Url', url)

    def __str__(self):
        return 'link'

