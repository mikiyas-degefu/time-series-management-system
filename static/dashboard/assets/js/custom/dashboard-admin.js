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
                    let card = $(`<div class="card"></div>`);
                    let cardBody = $(`
                            <div class="card-body">
                                <!--card header-->
                                <div class="d-flex align-items-center">
                                        
                                    <!--Indicator Title-->
                                    <div class="flex-grow-1 ms-3">
                                        <p class="mb-0"></p>
                                    </div>
            
                                    <!--Edit Button-->
                                    <div class="flex-shrink-0 ms-3">
                                        <div class="dropdown">
                                            <a class="avtar avtar-s btn-link-primary dropdown-toggle arrow-none" href="#" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                                <i class="ti ti-dots-vertical f-18"></i>
                                            </a>
                                            <div class="dropdown-menu dropdown-menu-end">
                                                <button 
                                                    type="button"
                                                    name="btn-edit" 
                                                    data-id="${draggable.data('id')}"
                                                    data-is-multiple="${draggable.data('isMultiple')}"
                                                    data-is-range="${draggable.data('isRange')}" 
                                                    data-bs-toggle="modal" 
                                                    data-bs-target="#modalAddDashboardRow" 
                                                    class="dropdown-item">
                                                    <svg class="pc-icon"> <use xlink:href="#custom-flash"></use></svg> 
                                                    Edit
                                                </button>
                                            </div>
                                        </div>
                                    </div>
            
                                </div>
        
                                
                            </div>
                    `);
                
                    // Clone the draggable and append it inside the parent div
                    cardBody.appendTo(card);
                    draggable.clone().appendTo(cardBody);
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
            drop: async function (event, ui) {
                let droppable = $(this); //get droppable element

                let rowId = await handleRowCreated(); //get row id from backend

                try {               
                   // Log the returned ID or handle if it is null
                   if (rowId) {
                    console.log("Returned ID: " + rowId);
                       // Create a new parent div (the row)
                    let parentDiv = $(`<div name="row" id="${rowId}" class="row p-5 border"><p>Drop Here</p></div>`);
            
                    // Append the parent div to the droppable element
                    parentDiv.appendTo(droppable);
            
                    handleAfterDropped();
                
                  
                   } else {
                     console.error("Failed to get ID");
                   }
            
                 } catch (error) {
                   console.error("Error during drop handling:", error);
                 }
            }
          });
    
        
    } );


    // Event delegation to handle dynamically added elements
    $(document).on('click', "[name='btn-edit']", function() {
        let isMultiple = $(this).data('isMultiple');
        let idRange = $(this).data('isRange');
        let componentId = $(this).data('id');

        //handle form type
        if(idRange == 'True'){
            $("#id_year").parent().hide()
            $("#id_data_range_start").parent().show()
            $("#id_data_range_end").parent().show()
        }else{
            $("#id_year").parent().show()
            $("#id_data_range_start").parent().hide()
            $("#id_data_range_end").parent().hide()
        }
        

        
        let isMultipleSelect = isMultiple == 'True' ? true : false; // Set your condition here

            if (isMultipleSelect) {
                $("#form-configuration").trigger("reset");
                $('#id_indicator').attr('multiple', 'multiple').addClass('form-select');

            } else {
                $("#form-configuration").trigger("reset");
                $('#id_indicator').removeAttr('multiple');
            }

        


    });



})