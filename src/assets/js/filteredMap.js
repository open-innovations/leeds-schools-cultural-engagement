// Some boiler plate to make a function that waits until the page is ready
(function(root){
	if(!root.OI) root.OI = {};
	if(!root.OI.ready){
		root.OI.ready = function(fn){
			// Version 1.1
			if(document.readyState != 'loading') fn();
			else document.addEventListener('DOMContentLoaded', fn);
		};
	}
})(window || this);

// Called when the page is ready
OI.ready(function(){

	// Create a function to add a functioning filter to a map
	function FilteredMap(boxid,attr){
		if(!attr) attr = {};
		var types = {},markers,dropdown;

		// Get the part of the page to add the filter to
		var box = document.getElementById(boxid);

		// Get the ID of the zoomable map we want
		var id = box.querySelector('.leaflet.leaflet-container').getAttribute('id');

		// Get the zoomable maps on the page
		var list = OI.ZoomableMap.get();

		// Use provided filters or leave empty
		filters = attr.filters||[];

		this.init = function(){

			var opt,_obj = this;

			// Get the markers
			markers = this.getMarkers();

			// Create a <select> element
			dropdown = document.createElement('select');

			// Add the <select> to the page
			if(attr.position=="after") box.append(dropdown);
			else box.prepend(dropdown);

			if(attr.label){
				var label = document.createElement('label');
				label.innerHTML = attr.label;
				label.setAttribute('for','filter');
				dropdown.before(label);
			}

			// If there are no filters we add some
			if(filters.length == 0){
				// Add default
				filters.push({
					'title':'All',
					'value':''
				});
				// Add 
				var fkeys = Object.keys(types).sort();
				for(var i = 0 ; i < fkeys.length; i++){
					filters.push({'title':fkeys[i]+' ('+types[fkeys[i]]+')','value':fkeys[i]});
				}
			}

			// Add each filter option to the <select>
			for(var i = 0; i < filters.length; i++){
				// Create an <option> element e.g. <option value="value">Text</option>
				opt = document.createElement('option');
				// Set the values
				opt.setAttribute('value',filters[i].value);
				opt.innerHTML = filters[i].title;
				dropdown.append(opt);
			}

			// Add a listener for when the dropdown value changes
			// It calls the function defined above
			dropdown.addEventListener('change',function(){ _obj.update(); });

			return this;
		};

		// Build an array of marker objects that reference the 
		// DOM element, tooltip and an array of engagement items
		this.getMarkers = function(){
			var map = list[id];
			var arr = [],tip,d,matches,i,l,e;

			// Get list items
			for(l = 0; l < map.layers.length; l++){
				if(map.layers[l].props.layer._layers){
					for(i in map.layers[l].props.layer._layers){
						if(map.layers[l].props.layer._layers[i]._popup._content){
							d = {
								'el': map.layers[l].props.layer._layers[i]._icon,
								'tooltip': map.layers[l].props.layer._layers[i]._popup._content,
								'engagement': []
							};
							tip = (d.tooltip||"");
							if(tip && typeof tip==="string"){
								if(typeof attr.parseTooltip==="function"){
									d.engagement = attr.parseTooltip.call(this,tip);
									for(e in d.engagement){
										if(typeof types[d.engagement[e]]==="undefined") types[d.engagement[e]] = 0;
										types[d.engagement[e]]++;
									}
								}
							}
							arr.push(d);
						}
					}
				}
			}
			return arr;
		};

		// Define a function to deal with the visitor changing the dropdown
		this.update = function(){
		
			// Here we have an array of "markers"
			var engagement,i,ok,tip,matches;
			for(i = 0; i < markers.length; i++){
				ok = false;
				if(dropdown.value==""){
					ok = true;
				}else{
					if(markers[i].engagement.includes(dropdown.value)) ok = true;
				}
				if(ok) markers[i].el.style.visibility = 'visible';
				else markers[i].el.style.visibility = 'hidden';
			}

			return this;
		};

		this.init();

		return this;
	}
	
	if(!OI.FilteredMap) OI.FilteredMap = FilteredMap;

});
