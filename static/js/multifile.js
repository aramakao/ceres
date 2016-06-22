function MultiSelector( list_target, max ){
	this.list_target = list_target;
	this.count = 0;
	this.id = 0;
	if( max ){
		this.max = max;
	} else {
		this.max = -1;
	};

	this.addElement = function( element ){

		if( element.tagName == 'INPUT' && element.type == 'file' ){

			element.name = 'file_' + this.id++;
			element.multi_selector = this;
			element.onchange = function(){

				var new_element = document.createElement( 'input' );
				new_element.type = 'file';
				this.parentNode.insertBefore( new_element, this );
				console.log(this.parentNode);
				this.multi_selector.addElement( new_element );
				this.multi_selector.addListRow( this );
				this.style.position = 'absolute';
				this.style.left = '-1000px';
			};
			if( this.max != -1 && this.count >= this.max ){
				element.disabled = true;
			};
			this.count++;
			this.current_element = element;
		} else {
			alert( 'Error: not a file input element' );
		};
	};
	this.addListRow = function( element ){
		var new_row = document.createElement( 'tr' );
		var img_td = document.createElement( 'td' );
		var name_td = document.createElement( 'td' );
		var button_td = document.createElement( 'td' );
		var new_row_button = document.createElement('button');
		new_row_button.type = 'button';
		new_row_button.innerHTML = '<i class="fa fa-trash-o"></i> Borrar';
		new_row_button.setAttribute("class", "btn btn btn-danger");

		var new_imagen= document.createElement('img');

    new_imagen.setAttribute("width", "304");
    new_imagen.setAttribute("height", "228");
		new_imagen.setAttribute("class", "img-thumbnail img-responsive");
		new_imagen.setAttribute("alt", element.value);
		if (element.files && element.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
					new_imagen.setAttribute("src",e.target.result);
        }
        reader.readAsDataURL(element.files[0]);
    }
		new_row.element = element;
		new_row_button.onclick= function(){
			this.parentNode.parentNode.element.parentNode.removeChild( this.parentNode.parentNode.element );
			this.parentNode.parentNode.parentNode.removeChild( this.parentNode.parentNode );
			this.parentNode.parentNode.element.multi_selector.count--;
			this.parentNode.parentNode.element.multi_selector.current_element.disabled = false;
			return false;
		};
		img_td.appendChild( new_imagen );
		name_td.innerHTML = element.value;
		button_td.appendChild( new_row_button );
		new_row.appendChild( img_td );
		new_row.appendChild( name_td );
		new_row.appendChild( button_td );
		this.list_target.appendChild( new_row );
	};
};
