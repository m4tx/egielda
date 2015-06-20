function Button(predecessor){
    // extends jQuery's button object
    for(var property in predecessor) {
        this[property] = predecessor[property];
    }

    this.enable = function() {
        predecessor.removeAttr('disabled');
    };

    this.disable = function() {
        predecessor.attr('disabled', 'disabled');
    };
}

function Edit(predecessor){
    // extends jQuery's text input object
    for(var property in predecessor) {
        this[property] = predecessor[property];
    }

    this.setText = function(text) {
        predecessor.val(text);
    };

    this.getText = function() {
        return predecessor.val();
    }
}

var get = function(expr) {
    var element = $(expr);
    if(element.is('input[type=button],button')) {
        return new Button(element);
    }
    if(element.is('input[type=text],input[type=number]')) {
        return new Edit(element);
    }
};