from flask import Flask, render_template, request, Blueprint
import sys

requestForPaymentBlueprint = Blueprint('requestForPaymentBlueprint', __name__)

@requestForPaymentBlueprint.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		return "{'Register'}"
		# return render_template('test.html')