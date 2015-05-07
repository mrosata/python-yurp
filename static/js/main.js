/*
 * This is to insert a category using Ajax from the /new page
jQuery(function ($) {
    var $categoryForm = $('#createCategoryForm');
    if ($categoryForm.length) {
        $categoryForm.on('submit.flasq', function (evt) {
            evt.preventDefault();
            // Send post request to add new category
            var url = $categoryForm.attr('action');
            var name = $('#newLabelName').val();

            data = {
                newLabelName: name
            };
            $.ajax({
                url: url,
                type: 'POST',
                data: data,
                done: function (res) {
                    console.log('done not answered: ', res)
                },
                success: function (res) {
                    console.log('got response: ', res)
                }
            });
        });
    }

});
*/

jQuery(function($){

    /***  Flash Message Modal Check */
    var $flashModal = $('#flashedMessages');
    if ($flashModal.length)
        $flashModal.modal('show');
    /* End Flash Message Modal Check */
    
    
    /***  Placeholders for the TextInputs  */
    var placeholderText = {
        'gist' : "Summary, idea, short, think Tweet",
        'content' : "Main content of the entry goes here..."
    }

    // Check for textareas and fill with initial content if empty
    $('textarea').on('blur.yurp', function (evt) {
        var $textarea = $(this);
        var name = $textarea.attr('name');
        if (name in placeholderText) {
            var currentVal = $(this).val();
            if (currentVal == '') {
                $(this).val(placeholderText[name]);
            }
        }

    });

    // Focus event to handle vanishing the placeholder text on click
    $('textarea').on('focus.yurp', function (evt) {
        var $textarea = $(this);
        var name = $textarea.attr('name');
        if (name in placeholderText) {
            var currentVal = $(this).val();
            if (currentVal == placeholderText[name]) {
                $(this).val('');
            }
        }
    });

    // Make sure on submit that no placeholder values are passed in form
    $('form').on('submit.yurp', function (evt) {
        $(this).find('textarea').each(function (ind, elm) {
            var name = $(elm).attr('name');
            if (name in placeholderText) {
                if ($(elm).val() == placeholderText[name] ) {
                    $(elm).val('');
                }
            }
        });
        return true;
    });

    // Trigger a blur to fill in initial state of the textareas
    $('textarea').trigger('blur.yurp');
});
