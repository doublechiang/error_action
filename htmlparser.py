import mammoth
import logging
from bs4 import BeautifulSoup


class HtmlParser:

    def importDocx(self, docx):
        with open(docx, 'rb') as docx_file:
            result = mammoth.convert_to_html(docx_file)
            self.html = result.value


    def getDictFromTable(self, **kwargs):
        """ header the criterial to match for the below content. 
        """
        header = kwargs.get('header')
        textonly = kwargs.get('textonly')
        soup = BeautifulSoup(self.html, 'html.parser')
        tables = soup.find_all('table')
        actions = {}
        for table in tables:
            tab_header = []
            # Get the header
            for tr in table.children:
                for th in tr.children:
                    tab_header.append(th.text)
                break
            if tab_header == header:
                logging.info(f'header match{header}')
                for sibling in table.tr.next_siblings:
                    content = []
                    key = None
                    for col in sibling:
                        if key is None:
                            key = col.text
                            continue
                        if textonly is not None:
                            content.append(col.text)
                        else:
                            content.append(col)
                    actions.update({key: content})
        
        return actions

    def __init__(self):
        pass





if __name__ == '__main__':
    h = HtmlParser()
    h.importDocx('C2190_Troubleshooting_v2_1.docx')
    # h.importDocx('test.docx')
    actions = h.getDictFromTable(header=['Repair Code', 'Repair Action'])
    print(actions.keys())
    err_actions = h.getDictFromTable(header=['ID', 'Content', 'Repair Code'], textonly=True)
    print(err_actions)