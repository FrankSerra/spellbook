$(document).ready(function(){
});

function editMode(value) {
	if(value == true)
    {
        addSpellParameter('edit', '1', false, true)
        $(".spellbook-edit").show();
    }        
    else
    {
        removeSpellParameter('edit', false, true)
        $(".spellbook-edit").hide();
    }
}

function gridMode(value) {
	if(value == true)
    {
        addSpellParameter('grid', '1', true, true)
    }        
    else
    {
        removeSpellParameter('grid', true, true)
    }
}