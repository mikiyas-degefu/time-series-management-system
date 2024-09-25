$(document).ready(()=>{
    $( function() {
       
        $("[name='component']").draggable({
            revert: "invalid",
            stack: ".draggable",
            helper: 'clone',
            scroll: false,
        });


        $("[name='row']").draggable({
            revert: "invalid",
            stack: ".draggable",
            helper: 'clone',
            scroll: false,
        });


        //col
        const handleAfterDropped = () =>{
            $('[name="row"]').droppable({
                accept: "[name='component']",
                drop: function (event, ui) {
                    let droppable = $(this);
                    let draggable = ui.draggable;

                    $(this).addClass( "bg-success" ).find( "p" ).html('');

                    //${draggable.data('size')}
            
                    // Create a new parent div
                    let parentDiv = $(`<div name="col_component" class="col-md-6 row-col"></div>`);
                    let card = $(`<div class="card p-1"></div>`);
            
                    // Clone the draggable and append it inside the parent div
                    draggable.clone().appendTo(card);
                    card.find('img').css('width', '100%');
                    card.find('img').css('height', '250px');
                    card.appendTo(parentDiv);
            
                    // Append the parent div to the droppable element
                    parentDiv.appendTo(droppable);

                    console.log(draggable.data('id'))
    
                    //draggable.css({top: '5px', left: '5px'});
                  

                    $( '[name="row"]' ).sortable({
                        items: '.row-col',
                        placeholder: "ui-state-highlight",
                    });

                    $( '[name="row"]').disableSelection(); //disable text selection on drag selection


                }
    
                
            });


        }



        //row
        $('#droppable2').droppable({
            accept: "[name='row']",
            drop: function (event, ui) {
                let droppable = $(this);
        
                // Create a new parent div
                let parentDiv = $('<div name="row" class="row border p-3"><p>Drop Here</p></div>');
        
        
                // Append the parent div to the droppable element
                parentDiv.appendTo(droppable);

                //save row
                handleRowCreated('4',4)

                //call to handle col
                handleAfterDropped()
                
            }    
        });
       


        //handle backend row created
        const handleRowCreated = (dashboard, row) =>{
            console.log(dashboard, row, "created")
        }
       
      
        
       

        
    } );
})