$(document).ready(function () {
    $('.payWithRazorpay').click(function (e) { 
        e.preventDefault();


        
        var first_name = $("[name='first_name']").val();
        var last_name = $("[name='last_name']").val();
        var email = $("[name='email']").val();
        var phone = $("[name='phone']").val();
        var address = $("[name='address_line_1']").val();
        var city = $("[name='city']").val();
        var state = $("[name='state']").val();
        var country = $("[name='country']").val();
        var order_note = $("[name='order_note']").val();
       var token = $("[name='csrfmiddlewaretoken']").val();
       console.log(token)
        var order_number = $('.order_number').attr('order_number');
       var grand_total = $('.grand_total').attr('grand-total');
        
       console.log(grand_total)
       console.log(order_number)

        // if(first_name == "" || last_name == "" || email == "" || phone == "" || address == "" || city == "" || state == "" || country == "" || order_note == "")
        // {
        //     alert("All fields are mandatory");
        //     console.log('all fields are mandatory')
        //     return false;
        // }else
        

       
        
            
                  
            var options = {
                "key": "rzp_test_YRIPc7w7gPnCKk", // Enter the Key ID generated from the Dashboard
                "amount": grand_total * 100 ,//response.total_price * 100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                "currency": "INR",
                "name": "Lovely",
                "description": "Thank you for buying from us",
                "image": "https://example.com/your_logo",
                // "order_id": "order_IluGWxBm9U8zJ8", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                "handler": function (responseb){
                    //  alert(responseb.razorpay_payment_id);
                    // alert(response.razorpay_order_id);
                    // alert(response.razorpay_signature)
                    data = {
                        'payment_mode':'Payment with Razorpay',
                        'payment_id':responseb.razorpay_payment_id,
                        'order_no':order_number,
                        'grand_total':grand_total,
                        csrfmiddlewaretoken: token 
                    }
                    $.ajax({
                        method: "POST",
                        url: "/orders/proceed-to-pay/",
                        data: data,
                        success: function (responsec) {
                            console.log('hai i m here');
                            swal(
                                'Congratulations!',
                                responsec.status,
                                'success'
                            ).then((value) => {

                                window.location.href = '/orders/order-completed'+'?order_number='+order_number
                                console.log(order_number)
                            });
                                
                        }
                    });
                },
                "prefill": {
                    "name": first_name + " " + last_name,
                    "email": email,
                    "contact": phone
                },
                "theme": {
                    "color": "#3399cc"
                }
            };
            var rzp1 = new Razorpay(options);
            rzp1.open();
                
            
            
        
         
        
    });
    //END OF RAZORPAY

    //CASH ON DELIVERY
    $('.cod').click(function (e) { 
        e.preventDefault();


        
        // var first_name = $("[name='first_name']").val();
        // var last_name = $("[name='last_name']").val();
        // var email = $("[name='email']").val();
        // var phone = $("[name='phone']").val();
        // var address = $("[name='address']").val();
        // var city = $("[name='city']").val();
        // var state = $("[name='state']").val();
        // var country = $("[name='country']").val();
        // var order_note = $("[name='order_note']").val();
        var token = $("[name='csrfmiddlewaretoken']").val();
        console.log(token)
        var order_number = $('.order_number').attr('order_number');
        var grand_total = $('.grand_total').attr('grand-total');
        
        console.log(grand_total)
        console.log(order_number)

        // if(first_name == "" || last_name == "" || email == "" || phone == "" || address == "" || city == "" || state == "" || country == "" || order_note == "")
        // {
        //     alert("All fields are mandatory");
        //     console.log('all fields are mandatory')
        //     return false;
        // }else
        
            
                   
        data = {
            'payment_mode':'Cash On Delivery',
            // 'payment_id':responseb.razorpay_payment_id,
            'order_no':order_number,
            'grand_total':grand_total,
            csrfmiddlewaretoken: token 
        }
        $.ajax({
            method: "POST",
            url: "/orders/proceed-to-pay/",
            data: data,
            success: function (responsec) {
                swal(
                    responsec.status,
                    'Congratulations!',
                    'success'
                ).then((value) => {

                    window.location.href = '/orders/order-completed'+'?order_number='+order_number
                    console.log(order_number)
                });
                    
            }
        });
                
            
            
        
         
        
    });


   
});