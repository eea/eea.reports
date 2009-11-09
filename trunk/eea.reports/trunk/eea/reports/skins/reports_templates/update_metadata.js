function toogle_field(obj, field_id){
    var field = document.getElementById(field_id);
    var auto_text = "(Automatically fill from publication pdf file metadata)"
    if(!field) return;

    old_value = field.old_value ? field.old_value : field.value != auto_text ? field.value : "";
    if(!obj.checked){
        field.value = old_value;
        field.readOnly = false;
    }else{
        field.old_value = field.value;
        field.value = auto_text;
        field.readOnly = true;
    }
}

function toggle_fields(obj){
    for(i=0;i<arguments.length;i++){
        toogle_field(obj, arguments[i]);
    }
}

function display_div(div_id, display){
    var div = document.getElementById(div_id);
    if (!div) return;
    div.style.display = display;
}

function file_changed(div_id, input_id){
    var field = document.getElementById(input_id);
    if (!field) return;

    display_div(div_id, 'block');
    toggle_fields(field, 'title', 'description');
}
