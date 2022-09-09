#!/usr/bin/env python3
from flask import Flask, request, redirect, render_template, url_for
import logging

from htmlparser import HtmlParser


app = Flask(__name__)
app.config['APPLICATION_ROOT'] = '/'

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Loading word/excel databse.
# err_dict = docxparser.DiagDocParser('DIAG Error Code Definitions V0.7.docx').getParsedDef()
# action_dict = repair_action.RepairActionParser('diag_database_latest.xlsx').getActionDef()

h = HtmlParser()
h.importDocx('C2190_Troubleshooting_v2_2_20220908.docx')
actions = h.getDictFromTable(header=['Repair Code', 'Repair Action'])
err_actions = h.getDictFromTable(header=['Error ID', 'Content', 'Repair Code'], textonly=True)



@app.route('/', methods=['get', 'post'])
def home():
    return redirect( url_for('error_main'))

@app.route('/error', methods=['get', 'post'])
@app.route('/error/', methods=['get', 'post'])
def error_main():
    if request.method == 'POST':
        err_code = request.form.get('err_code')
        return redirect(url_for('error_index', err_code=err_code))
    return render_template('search.html', err_code=None)

@app.route('/error/<err_code>')
def error_index(err_code):
    logger.debug(f"error_code is {err_code}")
    error = None
    action = None
    err_msg = None
    repair_code = None
    repair = err_actions.get(err_code)
    if repair is None:
        error = "error code is not define in our error database. Check administrator."
        logger.info(error)
    else:
        err_msg = repair[0]
        repair_code = repair[1]
        logger.info(f"repair code:{repair_code}")
        if repair_code is None:
            error = "Repair code is not defined in database."
            logger.info(error)
        else:
            action = actions.get(repair_code)
            if action is None:
                error = "Action is not defined in Repair database"
                logger.info(error)

    return render_template('search.html', error=error, err_code=err_code, err_msg=err_msg, repair_code=repair_code, action=action)
    




    

