/**
*
* Copyright (C) 2010 Ilshad R. Khabibullin <astoon.net at gmail.com>
*
* Ajax based BlueBream prompt.
*
**/

var LOAD_HISTORY =         '@@getControlDetailsREPLHistory';
var DOM_NODE_REPL =        'repl-wrapper';

var gREPLContainer;
var gREPL;

function REPL (context_url, action_url, parent) {
    this.context_url =  context_url;
    this.action_url =   action_url;
    this.parent =       parent;
    this.hist =         new Array();
    this.current =      0;
    this.formNode =     null;
    this.outputNode =   null;
}

REPL.prototype.loadForm = function () {
    var form = $('<form method="post" class="repl"></form>');
    form.submit(function () { return false });
    form.attr('action', this.action_url);

    var output = $('<div class="repl-output">&nbsp;</div>');
   
    form.append(output);
    form.append($('<span class="prompt-input">&gt;&gt;&gt;</span>'));

    var input = $('<input type="text" name="source" class="repl-input" />');
    input.attr('size', '68');
    input.attr('autocomplete', 'off');
    var repl = this;

    input.bind("keydown", function (event) {
	return repl.inputREPLKeydown(event.originalEvent)
    });
    form.append(input);
    $(this.parent).append(form);

    this.formNode = form[0];
    this.outputNode = output[0];
    input.focus();
}

REPL.prototype.loadHistory = function () {
    var repl = this;    
    $.ajax({type: "POST",
	    url: repl.context_url + LOAD_HISTORY,
	    dataType: "xml",
	    success: function (xml) {
		repl.hist = [];
		var doc = $('doc', xml);
		$('line', $(doc)).each(function (i) {
		    var txt = $(this).text();
		    repl.hist.push($(this).text());
//		    if (txt != "undefined" & txt != "undefine")
//			repl.history.push($(this).text());
		});
	    }});
}

REPL.prototype.fromHistory = function (ch) {
    this.current += ch;

    if (this.current == -1)
	this.current = this.hist.length - 1;

    if (this.current == this.hist.length)
	this.current = 0;

    return this.hist[this.current];
}

REPL.prototype.showLine = function (output, prompt) {
    switch (prompt) {
	case 'complete':
	var pr = '<span class="prompt" rel="complete">&gt;&gt;&gt;</span>';
	break;

	case 'incomplete':
	var last = $('span.prompt', this.outputNode.lastChild);
	if (last.length > 0) {
	    if (last.attr('rel') == 'complete')
		var pr = '<span class="prompt">&gt;&gt;&gt;</span>';
	    else
		var pr = '<span class="prompt">...</span>';
	} else {
	    var pr = '<span class="prompt">&gt;&gt;&gt;</span>';
	}
	break;

	default:
	var pr = '';
    }

    $('<div class="output">' + pr + '<pre>' + output + '</pre></div>'
     ).appendTo(this.outputNode);

    this.outputNode.scrollTop = this.outputNode.scrollHeight;
}

REPL.prototype.inputREPLKeydown = function (event) {
    var result = true;
    var action_url = this.action_url;

    //console.log(event);

    switch (event.keyCode) {
	/**
	 *
	 * enter - send the line
	 *
	 **/
	case 13:
	var value = event.target.value;
	var data = $(this.formNode).serialize();
	var repl = this;
	$.ajax({type: "POST",
		url: action_url,
		dataType: "xml",
		data: data,
		success: function (xml) {
		    var result = $('result', xml).text() == '0' ?
			'complete' : 'incomplete';
		    repl.showLine(value, result);
		    $('output > line', xml).each(function (i) {
			repl.showLine($(this).text(), null)
		    });
		}});
	this.loadHistory();
	event.target.value = '';
	break;


	/**
	 *
	 * tab indent
	 *
	 **/
	case 9:
	event.target.value += '    ';
	$(event.target).focus();
	result = false;
	break;


	/**
	 *
	 * up to history
	 *
	 **/
	case 38:
	var new_value = this.fromHistory(1);
	if (new_value) event.target.value = new_value;
	else event.target.value = '';
	break;


	/**
	 *
	 * down to history
	 *
	 **/
	case 40:
	var new_value = this.fromHistory(-1);
	if (new_value) event.target.value = new_value;
	else event.target.value = '';
	break;
    }
    return result;
}

// onload document
function loadform (context_url, action_url) {
    gREPLContainer = document.getElementById(DOM_NODE_REPL);
    gREPL = new REPL(context_url, action_url, gREPLContainer);
    gREPL.loadForm();
    gREPL.loadHistory();
}
