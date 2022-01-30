window.onload = function () {

    let quantity, price, order_item_num, delta_quantity, order_item_quantity, delta_cost;

    let quantity_arr = [];
    let price_arr = [];

    let total_forms = parseInt($('input[name=order_items-TOTAL_FORMS]').val());

    let order_total_quantity_container = $('.order_total_quantity');
    let order_total_cost_container = $('.order_total_cost');
    let order_total_quantity = parseInt(order_total_quantity_container.text()) || 0;
    let order_total_cost = parseInt(order_total_cost_container.text().replace(',', '.')) || 0;
    let order_form = $('.order_form');

    for (let i = 0; i < total_forms; i++) {
        quantity = parseInt($('input[name=order_items-' + i + '-quantity]').val());
        price = parseInt($('#order_items-' + i + '-price').text());

        quantity_arr[i] = quantity;
        if (price) {
            price_arr[i] = price;
        } else {
            price_arr[i] = 0;
        }
    }

    order_form.on('click', 'input[type=number]', function (event) {
            let target = event.target;
            order_item_num = parseInt(target.name.replace('order_items-', '').replace('-quantity', ''));
            if (price_arr[order_item_num]) {
                order_item_quantity = parseInt(target.value);
                delta_quantity = order_item_quantity - quantity_arr[order_item_num];
                quantity_arr[order_item_num] = order_item_quantity;
                orderSummaryUpdate(price_arr[order_item_num], delta_quantity);
            }
        }
    )

    order_form.on('click', 'input[type=checkbox]', function (event) {
            let target = event.target;
            order_item_num = parseInt(target.name.replace('order_items-', '').replace('-DELETE', ''));
            if (target.checked) {
                delta_quantity = -quantity_arr[order_item_num];
            } else {
                delta_quantity = quantity_arr[order_item_num];
            }
            orderSummaryUpdate(price_arr[order_item_num], delta_quantity);
        }
    );

    order_form.on('change', 'select', function (event) {
        let target = event.target;
        let order_item_num = parseInt(target.name.replace('order_items-', '').replace('-product', ''));
        let pk = target.value;
        let quantity_input = $('input[name=order_items-' + order_item_num + '-quantity]');
        let old_quantity = Number(quantity_input.val());
        if (pk) {
            $.ajax({
                type: "GET",
                url: '/orders/get_product_price/' + pk + '/',
                data: {},
                cache: false,

                success: function (data) {
                    if(old_quantity > 0) orderSummaryUpdate(price_arr[order_item_num], -old_quantity);

                    let new_quantity = 1;
                    price_arr[order_item_num] = Number(data.price);
                    quantity_input.val(new_quantity).attr('max', data.quantity);
                    quantity_arr[order_item_num] = new_quantity;
                    $('#order_items-' + order_item_num + '-price').html(data.price + '&nbsp;&#8381;');
                    orderSummaryUpdate(price_arr[order_item_num], new_quantity);
                },
                error: function (jqXHR) {
                    console.log('Что-то пошло не так!');
                }
            });
        } else {
            if(old_quantity > 0) orderSummaryUpdate(price_arr[order_item_num], -old_quantity);
            quantity_input.val('0').attr('max', 1);
            $('#order_items-' + order_item_num + '-price').html('');
            price_arr[order_item_num] = 0
            quantity_arr[order_item_num] = 0
        }
    });

    $('.formset_row').formset({
        addText: 'добавить продукт',
        deleteText: 'Удалить',
        prefix: 'order_items',
        removed: deleteOrderItem,
    });

    function orderSummaryUpdate(order_item_price, delta_quantity) {
        delta_cost = order_item_price * delta_quantity;
        order_total_cost = Number((order_total_cost + delta_cost).toFixed(2));
        order_total_quantity = order_total_quantity + delta_quantity;

        order_total_quantity_container.html(order_total_quantity.toString());
        order_total_cost_container.html(order_total_cost.toString() + '&nbsp;&#8381;');
    }

    function deleteOrderItem(row) {
        let target_name = row[0].querySelector('input[type="number"]').name;
        order_item_num = parseInt(target_name.replace('order_items-', '').replace('-quantity', ''));
        delta_quantity = -quantity_arr[order_item_num];
        orderSummaryUpdate(price_arr[order_item_num], delta_quantity);
    }

}