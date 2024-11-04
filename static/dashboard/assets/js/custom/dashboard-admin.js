$(document).ready(() => {
    $(function () {

        //generate unique id
        function* generateId() {
            let i = 0;
            while (true) {
                yield i++;
            }
        }

        const idGen = generateId();

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
        
        // Define handleAfterDropped function to handle element drop
        const handleAfterDropped = (event, ui) => {
            let droppable = $(event.target); // Target the specific row element
            let draggable = ui.draggable;
        
            droppable.addClass("bg-gray-300").find("h5").html("");
        
            let colId = idGen.next().value;
        
            // Create a new parent div for the column
            let parentDiv = $(`<div name="col_component" id="dragged_col_${colId}" class="col-md-4 row-col"></div>`);
            let card = $(`<div class="card"></div>`);
            let cardBody = $(`
                <div class="card-body">
                    <div class="d-flex align-items-center">
                        <div class="flex-grow-1 ms-3">
                            <p class="mb-0"></p>
                        </div>
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
                                        data-is-single-year="${draggable.data('isSingleYear')}"
                                        data-is-range="${draggable.data('isRange')}" 
                                        data-row-id="${droppable.attr('id')}"
                                        data-has-title="${draggable.data('hasTitle')}"
                                        data-has-indicator="${draggable.data('hasIndicator')}"
                                        data-has-description="${draggable.data('hasDescription')}"
                                        id="col_${colId}"
                                        data-bs-toggle="modal" 
                                        data-bs-target="#modalAddDashboardRow" 
                                        class="dropdown-item">
                                        <svg class="pc-icon"><use xlink:href="#custom-flash"></use></svg> 
                                        Edit
                                    </button>
        
                                    <!-- Col Delete Button -->
                                    <button 
                                        type="button" 
                                        name="btn-delete"
                                        id="delete_btn_col_${colId}"
                                        data-col-id="${colId}" 
                                        data-is-created="False"
                                        data-bs-toggle="modal" 
                                        data-bs-target="#removeComponent"
                                        class="dropdown-item">
                                        <i class="text-danger ti ti-x f-20 "></i>
                                        <span class="text-danger">Delete</span>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>`);
        
            // Append the cloned draggable and card structure
            cardBody.appendTo(card);
            draggable.clone().appendTo(cardBody);
            card.find('img').css('width', '100%');
            card.appendTo(parentDiv);
        
            // Append the parent div to the droppable element
            parentDiv.appendTo(droppable);
        
            // Make the columns sortable within each row
            droppable.sortable({
                items: '.row-col',
                placeholder: "ui-state-highlight",
            }).disableSelection();
        };
        
        // Apply droppable to the row container
        $('#droppable2').droppable({
            accept: "[name='row']",
            drop: async function (event, ui) {
                let droppable = $(this); // Get droppable element
                let rowId = await handleRowCreated(); // Get row id from backend
        
                if (rowId) {
                    let parentDiv = $(`
                        <div name="row" id="${rowId}" class="row p-5 border ui-droppable ui-sortable ui-draggable ui-draggable-handle">
                            
                            <div class="d-flex align-items-center justify-content-between mb-3">
                                <h5 class="mb-0"></h5>
                                <div class="dropdown">
                                    <a class="avtar avtar-s btn-link-secondary dropdown-toggle arrow-none" href="#" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        <i class="ti ti-dots-vertical f-18"></i>
                                    </a>
                                    <div class="dropdown-menu dropdown-menu-end">
                                        <a class="dropdown-item text-danger" href="#">Delete</a>
                                    </div>
                                </div>
                            </div>

                            <h5>Drop Here</h5>
                        </div>`);
                    parentDiv.appendTo(droppable);
                } else {
                    console.error("Failed to get ID");
                }
            }
        });
        
        $(document).on('drop', '[name="row"]', function(event, ui) {
            handleAfterDropped(event, ui);
        });
        
        $(document).on('mouseenter', '[name="row"]', function() {
            if (!$(this).data("droppable")) {
                $(this).droppable({
                    accept: "[name='component']"
                });
            }
        });
        


    // Event delegation to handle dynamically added elements
    $(document).on('click', "[name='btn-edit']", function () {
        let isMultiple = $(this).data('isMultiple');
        let isRange = $(this).data('isRange');
        let colId = $(this).attr('id');
        let hasTitle = $(this).data('hasTitle') == 'True' ? true : false
        let hasDescription = $(this).data('hasDescription') == 'True' ? true : false
        let isSingleYear = $(this).data('isSingleYear') == 'True' ? true : false
        let hasIndicator = $(this).data('hasIndicator') == 'True' ? true : false


        //handle form type
        if (isRange == 'True') {
            $("#id_year").parent().hide()
            $("#id_data_range_start").parent().show()
            $("#id_data_range_end").parent().show()
        } else {
            $("#id_year").parent().show()
            $("#id_data_range_start").parent().hide()
            $("#id_data_range_end").parent().hide()
        }

        hasTitle ? $("#id_title").show().prev().show() : $("#id_title").hide().prev().hide()
        hasDescription ? $("#id_description").show().prev().show() : $("#id_description").hide().prev().hide()
        isSingleYear ? $("#id_year").show().prev().show() : $("#id_year").hide().prev().hide()
        hasIndicator ? $("#id_indicator").show().prev().show() : $("#id_indicator").hide().prev().hide()



        let isMultipleSelect = isMultiple == 'True' ? true : false; // Set your condition here

        if (isMultipleSelect) {
            $("#form-configuration").trigger("reset");
            $('#id_indicator').attr('multiple', 'multiple').addClass('form-select');

        } else {
            $("#form-configuration").trigger("reset");
            $('#id_indicator').removeAttr('multiple').addClass('form-select');
        }


        //assign value to form
        $("#form_col_id").val(colId);


        //assign form value if exist
        let colIndicatorId = $(this).data('colIndicatorId') || null;
        let colYearId = $(this).data('colYearId') || null;
        let colWidth = $(this).data('colWidth') || null;
        let colTitle = $(this).data('colTitle') || null;
        let colDescription = $(this).data('colDescription') || null;
        let colDataRangeStart = $(this).data('colDataRangeStart') || null;
        let colDataRangeEnd = $(this).data('colDataRangeEnd') || null;

        $("#id_indicator").val(colIndicatorId)
        $("#id_year").val(colYearId);
        $("#id_width").val(colWidth);
        $("#id_title").val(colTitle);
        $("#id_description").val(colDescription);
        $("#id_data_range_start").val(colDataRangeStart);
        $("#id_data_range_end").val(colDataRangeEnd);

    });

    //handle on component remove 
    $(document).on('click', "[name='btn-delete']", function () {
        const colID = $(this).data('colId')
        const isCreated = $(this).data('isCreated')
        $('#delete_input_col_id').val(colID)
        $(`#delete_input_id_created`).val(isCreated)
    });


});
})
