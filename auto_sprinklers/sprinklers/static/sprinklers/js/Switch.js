(function($){

 $.fn.Switch = function(opt){
      if(typeof opt == 'undefined') opt = {};
        var 	_Switch_conf = $.extend({
				    'on':function(r){},
				    'off':function(r){},
				    'onConfirm':function(r){ return true;},
				    'offConfirm':function(r){ return true;},
				    'selected':function(r){},
				    'onTitle':'',
				    'responsive':false,
				    'offTitle':'',
				    'animate':true,
				    'offColor':'',
				    'onColor':'success',
				    'className':'',
				    'width':80
      },opt);
      if(opt == 'destroy'){
	  
	  this.each(function(){
	     if($(this).next().hasClass('Switch-switch-plugin-box') && $(this).hasClass('Switch-switch-plugin')){
		 $(this).next().remove();
		 $(this).css({'display':'inline-block'});
		  $(this).find('.Switch-switch-input').removeClass('Switch-switch-input');
		  
		 $(this).removeClass('Switch-switch-plugin');
	     } 
	  });
	  return false;
      }

    
      $.fn._radio_button_on = function(){
	     var __index = $(this).index('.Switch-switch-plugin');

	    var $thisElem = $(this);
	    
		$thisElem.css({'display':'none'});	 
	      
	      if(typeof _Switch_conf.checked != 'undefined'){
		  
		 if( _Switch_conf.checked.toString().substr(0,1) == '.'){
		    $thisElem.find('input'+_Switch_conf.checked+'').trigger("click");
		 }else{ 
		    $thisElem.find('input[value="'+_Switch_conf.checked+'"]').trigger("click");
		 }
		}
	    if($thisElem.hasClass('Switch-switch-plugin')){
		$(this).next().remove();
	    }
	 
	    var obj = [];
	    
	    var $inputElem = $thisElem.find('input').eq(0);
	     $thisElem.find('input').data({'_switch_opt':_Switch_conf});
	    var bootstrapContent  = '<div class="Switch '+(_Switch_conf.responsive == true ? ' switch-responsive ' : '' )+'  Switch-switch-plugin-box ';
	    
	    if(_Switch_conf.className != ''){
		  bootstrapContent+=_Switch_conf.className;
	      }
	      
	    bootstrapContent+='">';
		    
		    bootstrapContent+='<div class="Switch-switch-box '+(_Switch_conf.animate == true ? ' switch-animated-on ' : '')+'">';
	    if($inputElem.attr("type") == 'radio'){
		
		var $item = $thisElem.find('input[type="radio"]');
		if($item.length == 2){
		    $item.each(function(key,row){
			$(row).addClass('Switch-switch-input');
			var label = $(row).attr("data-title");
		    
			if(typeof label == 'undefined'){
			    if($(row).val() == '1' || $(row).attr("data-status") == '1' || $(row).attr("data-on") ){
				 
				label= _Switch_conf.onTitle;
			    }else{ 
				label= _Switch_conf.offTitle;
			    }
			}
			bootstrapContent+='<a class=" Switch-switch-item';
			
			if($(row).is(':checked')){
			    bootstrapContent+=' active ';
			    
			}
			if(!$item.is(':checked')){
				if($(row).val() == '0'){
				    bootstrapContent+=' active ';
				} 
			}
			
			if($(row).attr("data-on") || $(row).attr("data-status") == 'on' || $(row).attr("data-status") == '1'){
				bootstrapContent+=' Switch-switch-item-status-on ';
				if($(row).attr("data-on-color")){
					    
					    bootstrapContent+=' Switch-switch-item-color-'+$inputElem.attr("data-on-color");
				}else{
					    bootstrapContent+=' Switch-switch-item-color-'+_Switch_conf['onColor'];
				    
				}
				
			    }else{ 
			    if($(row).attr("data-off-color")){
					    
					    bootstrapContent+=' Switch-switch-item-color-'+$(row).attr("data-off-color");
				}else{ 
					    bootstrapContent+=' Switch-switch-item-color-'+_Switch_conf['offColor'];

				}
				bootstrapContent+=' Switch-switch-item-status-off ';
			    }
			bootstrapContent+='"';
			if(_Switch_conf.width != false && _Switch_conf.responsive == false){
			    _Switch_conf.width = parseInt(_Switch_conf.width);
			    bootstrapContent+=' style="width:'+_Switch_conf.width+'px !important" ';
			}
			bootstrapContent+=' >';
		    
			bootstrapContent+='<span class="lbl">'+label+'</span>'+'<span class="Switch-switch-cursor-selector"></span></a>';
		    });
		}
	    
	    }else if($inputElem.attr("type") == 'checkbox'){
			for(var i = 0;i<2;i++){
			$inputElem.addClass('Switch-switch-input');
			
			bootstrapContent+='<a class=" Switch-switch-item';
			if($inputElem.is(':disabled')){
			    bootstrapContent+=' disabled ';
			}
			    if(i == 0){
				if($inputElem.is(':checked')){
				    bootstrapContent+='  active ';
				    if($inputElem.attr("data-on-color")){
					    
					    bootstrapContent+=' Switch-switch-item-color-'+$inputElem.attr("data-on-color");
				    }else{ 
					    bootstrapContent+=' Switch-switch-item-color-'+_Switch_conf['onColor'];
				    }
				}
				bootstrapContent+='  Switch-switch-item-status-on';
			    }else{ 
			    if(!$inputElem.is(':checked')){
				    bootstrapContent+='  active ';
				}
				if($inputElem.attr("data-off-color")){
					    
					    bootstrapContent+=' Switch-switch-item-color-'+$inputElem.attr("data-off-color");
				    }else{ 
					bootstrapContent+=' Switch-switch-item-color-'+_Switch_conf['offColor'];

				    }
				bootstrapContent+='  Switch-switch-item-status-off';
			    }
			
			
			     
			 
			bootstrapContent+=' "';
			if(_Switch_conf.width != false && _Switch_conf.responsive == false){
			    _Switch_conf.width = parseInt(_Switch_conf.width);
			    bootstrapContent+=' style="width:'+_Switch_conf.width+'px !important" ';
			}
			bootstrapContent+='>';
			if(i == 0){
			    var label = $inputElem.attr("data-on-title");
			    if(typeof label == 'undefined'){
				    label= _Switch_conf.onTitle;
			    }
			}else{
			    var label = $inputElem.attr("data-off-title");
			    if(typeof label == 'undefined'){
				    label= _Switch_conf.offTitle;

			    }
			}
			
			bootstrapContent+='<span class="lbl">'+label+'</span>';
			    bootstrapContent+='<span class=" Switch-switch-cursor-selector"></span></a>';

			}
	    }
	    
	    
	    
	    
	    bootstrapContent+='</div>';					
	    bootstrapContent+='</div>';
	    $thisElem.after(function(){ return bootstrapContent});
	    var $thisElemNext = $thisElem.next();
	    
	    if($inputElem.attr("type") == 'radio'){
		    $thisElemNext.on('click','.Switch-switch-box',function(event,param){
			if(typeof param == 'undefined' && !param){
			    var param = false;
			}
			var selectedType = '';
			var $eElem =  $thisElemNext.find('.Switch-switch-item');
			var $activeItem = $(this).find('.active');
			if( $item.eq($eElem.not($activeItem).index()).attr('readonly') || $item.eq($eElem.not($activeItem).index()).is(':disabled')){
			    return;
			}
			if(  $item.eq($eElem.not($activeItem).index()).attr("data-off") || $item.eq($eElem.not($activeItem).index()).attr("data-status") == 'off' || $item.eq($eElem.not($activeItem).index()).attr("data-status") == '0'){
			    selectedType = 'off';
			    if(param == false && _Switch_conf.offConfirm($(this)) != true){
				return;
			    }
			}else{ 
						    selectedType = 'on';

			    if(param == false && _Switch_conf.onConfirm($(this)) != true){
				
				return;
			    }
			}
			
			$eElem.removeClass('active');
			$eElem.not($activeItem).addClass('active');
			
			
			var $newActive = $(this).find('.active');
			$item.eq($newActive.index()).prop('checked',true);
			_Switch_conf.selected($item.eq($newActive.index()),selectedType);
			 
		});
	    }else{ 
	    
		    $thisElemNext.on('click','.Switch-switch-box',function(event,param){
					    var selectedType = '';
    
		    var $eElem =  $thisElemNext.find('.Switch-switch-item');
			if(typeof param == 'undefined' && !param){
			    var param = false;
			}

			var $active = $thisElemNext.find('.active');
			    if( $inputElem.attr('readonly') || $inputElem.is(':disabled')){
			    return;
			}
			if($active.hasClass('Switch-switch-item-status-on')){
			    selectedType = 'off';
			    if(param == false && _Switch_conf.offConfirm($(this)) != true){
				    
				    return;
			    }
			}else{ 
						    selectedType = 'on';

			if(param == false && _Switch_conf.onConfirm($(this)) != true){
				    
				    return;
			    }
			}
			    if(!$inputElem.is(':disabled') && !$inputElem.attr('readonly')){
			    if($active.hasClass('Switch-switch-item-status-on')){
				
				$active.removeClass('active');
				$eElem.not($active).addClass('active');
				_Switch_conf.off($thisElemNext);
			    }else if($active.hasClass('Switch-switch-item-status-off')){
				 
				$active.removeClass('active');
				$eElem.not($active).addClass('active');
				_Switch_conf.on($thisElemNext);
			    }
			    $inputElem.trigger("click");
			    _Switch_conf.selected($inputElem,selectedType);
			    }
			    
			    

		    });
	    }
	    
	  
      };
      var _g = [];
    return   this.each(function(){
		$(this).addClass('Switch-switch-plugin');
	
	    $(this)._radio_button_on();
      });
    
        
  }
    $(document).ready(function() {
	  $(document).on('click change','.Switch-switch-input',function(event){
	    var $this = $(this).parent();
		$this.Switch($(this).data("_switch_opt"));
	    
	  });
      }); 
  }( jQuery ));
