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
        self.__xml = ElementTree.fromstring(serialized_xml)
        self.__ToUserName = self.__xml.find('ToUserName').text
        self.__FromUserName = self.__xml.find('FromUserName').text
        self.__CreateTime = int(self.__xml.find('CreateTime').text)
        self.__MsgId = int(self.__xml.find('MsgId').text)

    def __setup_filed(self):
        self.__xml = None
        self.__ToUserName = None
        self.__FromUserName = None
        self.__CreateTime = None
        self.__MsgId = None

    @property
    def to_user_name(self):
        return self.__ToUserName

    @to_user_name.setter
    def to_user_name(self, name):
        self.__ToUserName = name
        self.__set_text('ToUserName', name)

    @property
    def from_user_name(self):
        return self.__FromUserName

    @from_user_name.setter
    def from_user_name(self, name):
        self.__FromUserName = name
        self.__set_text('FromUserName', name)

    @property
    def create_time(self):
        return self.__CreateTime

    @create_time.setter
    def create_time(self, time):
        self.__CreateTime = time
        self.__set_text('CreateTime', str(time))

    @property
    def msg_id(self):
        return self.__MsgId

    @msg_id.setter
    def msg_id(self, package_id):
        self.__MsgId = package_id
        self.__set_text('MsgId', str(package_id))

    def dump(self):
        msg_type = self.__xml.find('MsgType')
        if msg_type is None:
            msg_type = ElementTree.SubElement(self.__xml, 'MsgType')
        msg_type.text = str(self.__class__)
        return ElementTree.dump(self.__xml)

    def __create_empty_tree(self):
        root = ElementTree.Element('xml')
        ElementTree.SubElement(root, 'ToUserName')
        ElementTree.SubElement(root, 'FromUserName')
        ElementTree.SubElement(root, 'CreateTime')
        ElementTree.SubElement(root, 'MsgId')
        self.__xml = root

    def __set_text(self, section, text):
        self.__xml.find(section).text = text


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
        return self.__Content

    @content.setter
    def content(self, text):
        self.__Content = text
        self.__set_text('Content', text)

    def __setup_filed(self):
        self.__Content = None

    def __import_tree(self, serialized_xml):
        self.__Content = self.__xml.find('Content').text

    def __create_empty_tree(self):
        ElementTree.SubElement(self.__xml, 'Content')


class media(base_message):

    def __init__(self, serialized_xml):
        super(media, self).__init__(serialized_xml)

        self.__setup_filed()
        if serialized_xml is not None:
            self.__import_tree(serialized_xml)
        else:
            self.__create_empty_tree()

    def __setup_filed(self):
        self.__MediaId = None

    def __import_tree(self, serialized_xml):
        self.__MediaId = self.__xml.find('MediaId').text

    def __create_empty_tree(self):
        ElementTree.SubElement(self.__xml, 'MediaId')

    @property
    def media_id(self):
        return self.__MediaId

    @media_id.setter
    def media_id(self, id):
        self.__MediaId = id
        self.__set_text('MediaId', id)


class image(media):

    def __init__(self, serialized_xml):
        super(image, self).__init__(serialized_xml)

        self.__setup_filed()
        if serialized_xml is not None:
            self.__import_tree(serialized_xml)
        else:
            self.__create_empty_tree()

    def __setup_filed(self):
        self.__PicUrl = None

    def __import_tree(self, serialized_xml):
        self.__PicUrl = self.__xml.find('PicUrl').text

    def __create_empty_tree(self):
        ElementTree.SubElement(self.__xml, 'PicUrl')

    @property
    def picture_url(self):
        return self.__PicUrl

    @picture_url.setter
    def picture_url(self, url):
        self.__PicUrl = url
        self.__set_text('PicUrl', url)


class voice(media):

    def __init__(self, serialized_xml):
        super(voice, self).__init__(serialized_xml)

        self.__setup_filed()
        if serialized_xml is not None:
            self.__import_tree(serialized_xml)
        else:
            self.__create_empty_tree()

    def __setup_filed(self):
        self.__Format = None
        self.__Recognition = None

    def __import_tree(self, serialized_xml):
        self.__Format = self.__xml.find('Format').text
        self.__Recognition = self.__xml.find('Recognition').text

    def __create_empty_tree(self):
        ElementTree.SubElement(self.__xml, 'Format')
        ElementTree.SubElement(self.__xml, 'Recognition')

    @property
    def format(self):
        return self.__Format

    @format.setter
    def format(self, ft):
        self.__Format = ft
        self.__set_text('Format', ft)

    @property
    def recognition(self):
        return self.__Recognition

    @recognition.setter
    def recognition(self, re):
        self.__Recognition = re
        self.__set_text('Recognition', re)


class video(media):

    def __init__(self, serialized_xml):
        super(video, self).__init__(serialized_xml)

        self.__setup_filed()
        if serialized_xml is not None:
            self.__import_tree(serialized_xml)
        else:
            self.__create_empty_tree()

    def __setup_filed(self):
        self.__ThumbMediaId = None

    def __import_tree(self, serialized_xml):
        self.__ThumbMediaId = self.__xml.find('ThumbMediaId').text

    def __create_empty_tree(self):
        ElementTree.SubElement(self.__xml, 'ThumbMediaId')

    @property
    def thumb(self):
        return self.__ThumbMediaId

    @thumb.setter
    def thumb(self, media_id):
        self.__ThumbMediaId = media_id
        self.__set_text('ThumbMediaId', media_id)


class shortvideo(video):
    pass


class location(base_message):

    def __init__(self, serialized_xml):
        super(location, self).__init__(serialized_xml)

        self.__setup_filed()
        if serialized_xml is not None:
            self.__import_tree(serialized_xml)
        else:
            self.__create_empty_tree()

    def __setup_filed(self):
        self.__Location_X = None
        self.__Location_Y = None
        self.__Scale = None
        self.__Lable = None

    def __import_tree(self, serialized_xml):
        self.__Location_X = float(self.__xml.find('Location_X').text)
        self.__Location_Y = float(self.__xml.find('Location_Y').text)
        self.__Scale = float(self.__xml.find('Scale').text)
        self.__Lable = self.__xml.find('Label').text

    def __create_empty_tree(self):
        ElementTree.SubElement(self.__xml, 'Location_X')
        ElementTree.SubElement(self.__xml, 'Location_Y')
        ElementTree.SubElement(self.__xml, 'Scale')
        ElementTree.SubElement(self.__xml, 'Label')

    @property
    def location_x(self):
        return self.__Location_X

    @location_x.setter
    def location_x(self, pos):
        self.__Location_X = pos
        self.__set_text('Location_X', str(pos))

    @property
    def location_y(self):
        return self.__Location_Y

    @location_y.setter
    def location_y(self, pos):
        self.__Location_Y = pos
        self.__set_text('Location_Y', str(pos))

    @property
    def scale(self):
        return self.__Scale

    @scale.setter
    def scale(self, scale):
        self.__Scale = scale
        self.__set_text('Scale', str(scale))

    @property
    def label(self):
        return self.__Lable

    @label.setter
    def label(self, text):
        self.__Lable = text
        self.__set_text('Label', text)


class link(base_message):

    def __init__(self, serialized_xml=None):
        super(link, self).__init__()

        self.__setup_filed()
        if serialized_xml is not None:
            self.__import_tree(serialized_xml)
        else:
            self.__create_empty_tree()

    def __setup_filed(self):
        self.__Title = None
        self.__Description = None
        self.__Url = None

    def __import_tree(self, serialized_xml):
        self.__Title = self.__xml.find('Title').text
        self.__Description = self.__xml.find('Description').text
        self.__Url = self.__xml.find('Url').text

    def __create_empty_tree(self):
        ElementTree.SubElement(self.__xml, 'Title')
        ElementTree.SubElement(self.__xml, 'Description')
        ElementTree.SubElement(self.__xml, 'Url')

    @property
    def title(self):
        return  self.__Title

    @title.setter
    def title(self, text):
        self.__Title = text
        self.__set_text('Title', text)

    @property
    def description(self):
        return self.__Description

    @description.setter
    def description(self, text):
        self.__Description = text
        self.__set_text('Description', text)

    @property
    def url(self):
        return self.__Url

    @url.setter
    def url(self, url):
        self.__Url = url
        self.__set_text('Url', url)
