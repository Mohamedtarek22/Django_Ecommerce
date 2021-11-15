$(document).ready(function(){
$(document).on('click',".add-to-cart",function(){
    var _vm=$(this);
    var _index=_vm.attr('data-index')
    var _qty=$(".product-qty-"+_index).val();
    var _productId=$(".product-id-"+_index).val();
    var _productImage=$(".product-image-"+_index).val();
    var _productTitle=$(".product-title-"+_index).val();
    var _productPrice=$(".product-price-"+_index).text();


    console.log(_qty,_productId,_productTitle,_productPrice)


    $.ajax({
        url:'/add-to-cart',
        data:{
            'id':_productId,
            'image':_productImage,
            'qty':_qty,
            'title':_productTitle,
            'price':_productPrice
        },
        dataType:'json',
        beforeSend:function(){
            _vm.attr('disabled',true);
        },
        success:function(res){
            console.log(res)
            $(".cart-list").text(res.totalitems);
            _vm.attr('disabled',false);
        }
    });

})
// addwishlist
$(document).on('click',".add-wishlist",function(){
    var _pid=$(this).attr('data-product');
    var _vm=$(this)
    // console.log(_pid)
    //Ajax
    $.ajax({
        url:"/add-wishlist",
        data:{
            product:_pid
        },
        dataType:'json',
        success:function(res){
            // console.log(res)
            if(res.bool==true){
                _vm.addClass('disabled').removeClass('add-wishlist')
            }
        }
    })
    //end

})
$(document).on('click','.delete-item',function(){
    var _pId=$(this).attr('data-item');
    var _vm=$(this);
    // Ajax
    $.ajax({
        url:'/delete-from-cart',
        data:{
            'id':_pId,
        },
        dataType:'json',
        beforeSend:function(){
            _vm.attr('disabled',true);
        },
        success:function(res){
            $(".cart-list").text(res.totalitems);
            _vm.attr('disabled',false);
            $("#cartList").html(res.data);
        }
    });
    // End
});
$(document).on('click','.update-item',function(){
    var _pId=$(this).attr('data-item');
    var _pQty=$(".product-qty-"+_pId).val();

    var _vm=$(this);
    // Ajax
    $.ajax({
        url:'/update-cart',
        data:{
            'id':_pId,
            'qty':_pQty
        },
        dataType:'json',
        beforeSend:function(){
            _vm.attr('disabled',true);
        },
        success:function(res){
            // $(".cart-list").text(res.totalitems);
            _vm.attr('disabled',false);
            $("#cartList").html(res.data);
        }
    });
    // End
});
$(document).on('click','.activate-address',function(){
    var _aId=$(this).attr('data-address');
    var _vm=$(this);
    // Ajax
    $.ajax({
        url:'/activate-address',
        data:{
            'id':_aId,
        },
        dataType:'json',
        beforeSend:function(){
            _vm.attr('disabled',true);
        },
        success:function(res){
            // console.log(res)
            if (res.bool==true){
                $(".address").removeClass('shadow border-secondary')
                $(".address"+_aId).addClass('shadow border-secondary')
                $(".check").remove()
                $(".activated"+_aId).html('<i class=" fa fa-check-circle text-success check"></i>')
                location.reload()
            }
        }
    });
    // End
});


});
