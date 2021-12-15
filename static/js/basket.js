$(document).ready(function () {
    initBasketQuantity();
});

function initBasketQuantity() {

    $('.plus button, .minus button').each(function () {

        $(this).on('click', function () {

            let container = $(this).closest('.quantity-container'),
                quantity_div = container.find('.quantity'),
                pk = quantity_div.attr('data-pk'),
                max_quantity = quantity_div.attr('data-max'),
                mode = $(this).closest('div').hasClass('plus') ? 'plus' : 'minus',
                old_quantity = Number(quantity_div.html()),
                new_quantity = mode === 'plus' ? old_quantity + 1 : old_quantity - 1;

            if (new_quantity >= 1 && new_quantity <= max_quantity) {
                $.ajax({
                    type: "GET",
                    url: '/basket/update_quantity/'+pk,
                    data: {quantity: new_quantity},
                    cache: false,

                    success: function (data) {
                        quantity_div.html(new_quantity);
                        $('#product_cost'+pk).html(data.product_cost);
                        $('#basket_total_quantity').html(data.total_quantity);
                        $('#basket_total_cost').html(data.total_cost);
                        $('#top_total_quantity').html(data.total_quantity);
                        $('#top_total_cost').html(data.total_cost);
                    },
                    error: function (jqXHR) {
                        alert('Что-то пошло не так!');
                    }
                });
            }
        });


    });
}