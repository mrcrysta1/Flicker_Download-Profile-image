<!DOCTYPE html>
<html lang="en">


<head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <title>Contact Me</title>

    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" integrity="sha512-9usAa10IRO0HhonpyAIVpjrylPvoDwiPUiKdWk5t3PyolY1cOd4DSE0Ga+ri4AuTroPR5aQvXU9xC6qOPnzFeg==" crossorigin="anonymous" referrerpolicy="no-referrer" />
    <!-- <link href="aos/aos.css" rel="stylesheet"> -->
    <link rel="stylesheet" href="css/bootstrap.min.css">
    <link rel="stylesheet" href="css/style.css" />

</head>

<body>
    <header class="header">
        <nav class="navbar">
            <ul class="navbar-lists" style="float: right; margin: 3rem;
            position: relative;
            bottom: 3rem;
            left: 38rem;
            z-index: 8;">

                <img src="img/logo.png" alt="" class="logo" />

            </ul>
        </nav>

        <div class="mobile-navbar-btn ">
            <ion-icon class="mobile-nav-icon " name="menu-outline " class="mobile-nav-icon "></ion-icon>

            <ion-icon class="mobile-nav-icon " name="close-outline " class="mobile-nav-icon "></ion-icon>
        </div>
    </header>


    <!-- ======================================== 
          Our  Cotnact Us Section   
    ========================================  -->
    <section class="section section-contact">
        <div class="container">
            <h2 class="common-heading h_dark">Email us</h2>
        </div>

        <div id="hireme" class="section-contact-main contact-container">
            <form action="" method="POST">
                <div class="grid grid-two-col">
                    <input type="text" name="username" value="" id="" required placeholder="Name*">
                    <input type="email" name="email" value="" required placeholder="Email*" autocomplete="false">
                </div>
                <div>
                    <input type="text" value="" name="subject" placeholder="Subject">
                </div>
                <div>
                    <textarea name="message" id="" placeholder="Message*"></textarea>
                </div>

                <div>
                    <input type="submit" name="submit" value="send message" class=" btn">
                </div>
                <?php
                //Define name spaces
                use PHPMailer\PHPMailer\PHPMailer;
                use PHPMailer\PHPMailer\SMTP;
                use PHPMailer\PHPMailer\Exception;
                //Create instance of PHPMailer
                require 'includes/PHPMailer.php';
                require 'includes/SMTP.php';
                require 'includes/Exception.php';

                if (isset($_POST['submit'])) {
                    $username = $_POST['username'];
                    $email = $_POST['email'];
                    $html1 = "<!DOCTYPE html>
                    <html xmlns:v='urn:schemas-microsoft-com:vml' xmlns:o='urn:schemas-microsoft-com:office:office' lang='en'> <head>
                        <title></title>
                        <meta http-equiv='Content-Type' content='text/html; charset=utf-8'>
                        <meta name='viewport' content='width=device-width, initial-scale=1.0'><!--[if mso]><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch><o:AllowPNG/></o:OfficeDocumentSettings></xml><![endif]--><!--[if !mso]><!-->
                        <link href='https://fonts.googleapis.com/css?family=Noto+Serif' rel='stylesheet' type='text/css'>
                        <link href='https://fonts.googleapis.com/css2?family=Inter&amp;family=Work+Sans:wght@700&amp;display=swap' rel='stylesheet' type='text/css'><!--<![endif]-->
                        <style>
                            * {
                                box-sizing: border-box;
                            }
                    
                            body {
                                margin: 0;
                                padding: 0;
                            }
                    
                            a[x-apple-data-detectors] {
                                color: inherit !important;
                                text-decoration: inherit !important;
                            }
                    
                            #MessageViewBody a {
                                color: inherit;
                                text-decoration: none;
                            }
                    
                            p {
                                line-height: inherit
                            }
                    
                            .desktop_hide,
                            .desktop_hide table {
                                mso-hide: all;
                                display: none;
                                max-height: 0px;
                                overflow: hidden;
                            }
                    
                            .image_block img+div {
                                display: none;
                            }
                    
                            @media (max-width:720px) {
                                .desktop_hide table.icons-inner {
                                    display: inline-block !important;
                                }
                    
                                .icons-inner {
                                    text-align: center;
                                }
                    
                                .icons-inner td {
                                    margin: 0 auto;
                                }
                    
                                .row-content {
                                    width: 100% !important;
                                }
                    
                                .mobile_hide {
                                    display: none;
                                }
                    
                                .stack .column {
                                    width: 100%;
                                    display: block;
                                }
                    
                                .mobile_hide {
                                    min-height: 0;
                                    max-height: 0;
                                    max-width: 0;
                                    overflow: hidden;
                                    font-size: 0px;
                                }
                    
                                .desktop_hide,
                                .desktop_hide table {
                                    display: table !important;
                                    max-height: none !important;
                                }
                    
                                .row-6 .column-2 .block-1.heading_block h1,
                                .row-6 .column-2 .block-2.heading_block h1,
                                .row-6 .column-2 .block-3.paragraph_block td.pad>div {
                                    text-align: center !important;
                                }
                    
                                .row-2 .column-1,
                                .row-4 .column-1 {
                                    padding: 20px 10px !important;
                                }
                    
                                .row-2 .column-2 {
                                    padding: 5px 25px 20px !important;
                                }
                    
                                .row-6 .column-1 {
                                    padding: 15px 25px 0 !important;
                                }
                    
                                .row-6 .column-2 {
                                    padding: 15px 20px 25px !important;
                                }
                            }
                        </style>
                    </head>
                    
                    <body style='background-color: #ffffff; margin: 0; padding: 0; -webkit-text-size-adjust: none; text-size-adjust: none;'>
                        <table class='nl-container' width='100%' border='0' cellpadding='0' cellspacing='0' role='presentation' style='mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #ffffff;'>
                            <tbody>
                                <tr>
                                    <td>
                                        <table class='row row-1' align='center' width='100%' border='0' cellpadding='0' cellspacing='0' role='presentation' style='mso-table-lspace: 0pt; mso-table-rspace: 0pt;'>
                                            <tbody>
                                                <tr>
                                                    <td>
                                                        <table class='row-content stack' align='center' border='0' cellpadding='0' cellspacing='0' role='presentation' style='mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; border-radius: 0; width: 700px;' width='700'>
                                                            <tbody>
                                                                <tr>
                                                                    <td class='column column-1' width='100%' style='mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 5px; padding-top: 5px; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;'>
                                                                        <div class='spacer_block block-1' style='height:15px;line-height:15px;font-size:1px;'>&#8202;</div>
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        <table class='row row-2' align='center' width='100%' border='0' cellpadding='0' cellspacing='0' role='presentation' style='mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #ffffff;'>
                                            <tbody>
                                                <tr>
                                                    <td>
                                                        <table class='row-content stack' align='center' border='0' cellpadding='0' cellspacing='0' role='presentation' style='mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; border-radius: 0; background-image: url(https://d1oco4z2z1fhwp.cloudfront.net/templates/default/7836/Header-bg.png); background-repeat: no-repeat; background-size: cover; background-color: #012970; width: 700px;' width='700'>
                                                            <tbody>
                                                                <tr>
                                                                    <td class='column column-1' width='25%' style='mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 20px; padding-left: 30px; padding-right: 10px; padding-top: 20px; vertical-align: middle; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;'>
                                                                        <table class='image_block block-1' width='100%' border='0' cellpadding='0' cellspacing='0' role='presentation' style='mso-table-lspace: 0pt; mso-table-rspace: 0pt;'>
                                                                            <tr>
                                                                                <td class='pad' style='width:100%;padding-right:0px;padding-left:0px;'>
                                                                                    <div class='alignment' align='center' style='line-height:10px'><a href='https://www.example.com' target='_blank' style='outline:none' tabindex='-1'><img src='https://d15k2d11r6t6rl.cloudfront.net/public/users/Integrators/BeeProAgency/962974_947526/logo2.png' style='display: block; height: auto; border: 0; width: 135px; max-width: 100%;' width='135' alt='' title='your-logo'></a></div>
                                                                                </td>
                                                                            </tr>
                                                                        </table>
                                                                    </td>
                                                                    <td class='column column-2' width='75%' style='mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 5px; padding-left: 25px; padding-right: 30px; padding-top: 5px; vertical-align: middle; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;'>
                                                                        <table class='empty_block block-1' width='100%' border='0' cellpadding='0' cellspacing='0' role='presentation' style='mso-table-lspace: 0pt; mso-table-rspace: 0pt;'>
                                                                            <tr>
                                                                                <td class='pad'>
                                                                                    <div></div>
                                                                                </td>
                                                                            </tr>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        <table class='row row-3' align='center' width='100%' border='0' cellpadding='0' cellspacing='0' role='presentation' style='mso-table-lspace: 0pt; mso-table-rspace: 0pt;'>
                                            <tbody>
                                                <tr>
                                                    <td>
                                                        <table class='row-content stack' align='center' border='0' cellpadding='0' cellspacing='0' role='presentation' style='mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #efeef4; border-bottom: 0 solid #EFEEF4; border-left: 0 solid #EFEEF4; border-right: 0px solid #EFEEF4; border-top: 0 solid #EFEEF4; color: #000000; width: 700px;' width='700'>
                                                            <tbody>
                                                                <tr>
                                                                    <td class='column column-1' width='100%' style='mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 25px; padding-left: 25px; padding-right: 25px; padding-top: 35px; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;'>
                                                                        <table class='heading_block block-1' width='100%' border='0' cellpadding='0' cellspacing='0' role='presentation' style='mso-table-lspace: 0pt; mso-table-rspace: 0pt;'>
                                                                            <tr>
                                                                                <td class='pad' style='padding-top:10px;text-align:center;width:100%;'>
                                                                                    <h1 style='margin: 0; color: #012970; direction: ltr; font-family: 'Noto Serif', Georgia, serif; font-size: 41px; font-weight: 700; letter-spacing: normal; line-height: 120%; text-align: center; margin-top: 0; margin-bottom: 0;'><span class='tinyMce-placeholder'>";
                    $subject = $_POST['subject'];
                    $html2 = "</span></h1>
                    </td>
                </tr>
            </table>
            <table class='paragraph_block block-2' width='100%' border='0' cellpadding='0' cellspacing='0' role='presentation' style='mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;'>
                <tr>
                    <td class='pad' style='padding-left:10px;padding-right:10px;'>
                        <div style='color:#201f42;direction:ltr;font-family:Inter, sans-serif;font-size:16px;font-weight:400;letter-spacing:0px;line-height:180%;text-align:center;mso-line-height-alt:28.8px;'>
                            <p style='margin: 0;'>";
                    $message = $_POST['message'];
                    $html3 = "</p>
                    </div>
                </td>
            </tr>
        </table>
    </td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table class='row row-4' align='center' width='100%' border='0' cellpadding='0' cellspacing='0' role='presentation' style='mso-table-lspace: 0pt; mso-table-rspace: 0pt;'>
<tbody>
<tr>
<td>
<table class='row-content stack' align='center' border='0' cellpadding='0' cellspacing='0' role='presentation' style='mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-image: url(https://d1oco4z2z1fhwp.cloudfront.net/templates/default/7836/Header-bg.png); background-repeat: no-repeat; background-size: cover; border-radius: 0; color: #000000; width: 700px;' width='700'>
<tbody>
<tr>
    <td class='column column-1' width='100%' style='mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 25px; padding-left: 10px; padding-right: 10px; padding-top: 25px; vertical-align: middle; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;'>
        <div class='spacer_block block-1' style='height:60px;line-height:60px;font-size:1px;'>&#8202;</div>
    </td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table class='row row-5' align='center' width='100%' border='0' cellpadding='0' cellspacing='0' role='presentation' style='mso-table-lspace: 0pt; mso-table-rspace: 0pt;'>
<tbody>
<tr>
<td>
<table class='row-content stack' align='center' border='0' cellpadding='0' cellspacing='0' role='presentation' style='mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #ffffff; color: #000000; width: 700px;' width='700'>
<tbody>
<tr>
    <td class='column column-1' width='100%' style='mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 35px; padding-left: 30px; padding-right: 30px; padding-top: 50px; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;'>
        <table class='heading_block block-1' width='100%' border='0' cellpadding='0' cellspacing='0' role='presentation' style='mso-table-lspace: 0pt; mso-table-rspace: 0pt;'>
            <tr>
                <td class='pad' style='text-align:center;width:100%;'>
                    <h2 style='margin: 0; color: #201f42; direction: ltr; font-family: 'Noto Serif', Georgia, serif; font-size: 24px; font-weight: 700; letter-spacing: normal; line-height: 120%; text-align: center; margin-top: 0; margin-bottom: 0;'><u><span class='tinyMce-placeholder'>Contact Us</span></u></h2>
                </td>
            </tr>
        </table>
    </td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table class='row row-6' align='center' width='100%' border='0' cellpadding='0' cellspacing='0' role='presentation' style='mso-table-lspace: 0pt; mso-table-rspace: 0pt;'>
<tbody>
<tr>
<td>
<table class='row-content stack' align='center' border='0' cellpadding='0' cellspacing='0' role='presentation' style='mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #ffffff; color: #000000; border-bottom: 0 solid #EFEEF4; border-left: 0 solid #EFEEF4; border-right: 0px solid #EFEEF4; border-top: 0 solid #EFEEF4; width: 700px;' width='700'>
<tbody>
<tr>
    <td class='column column-1' width='33.333333333333336%' style='mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 25px; padding-left: 25px; padding-right: 25px; padding-top: 15px; vertical-align: middle; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;'>
        <table class='image_block block-1' width='100%' border='0' cellpadding='15' cellspacing='0' role='presentation' style='mso-table-lspace: 0pt; mso-table-rspace: 0pt;'>
            <tr>
                <td class='pad'>
                    <div class='alignment' align='center' style='line-height:10px'><a href='https://www.example.com' target='_blank' style='outline:none' tabindex='-1'><img src='https://d1oco4z2z1fhwp.cloudfront.net/templates/default/7836/contact-01.png' style='display: block; height: auto; border: 0; width: 153px; max-width: 100%;' width='153' alt='alumni member' title='alumni member'></a></div>
                </td>
            </tr>
        </table>
    </td>
    <td class='column column-2' width='66.66666666666667%' style='mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 25px; padding-left: 5px; padding-right: 20px; padding-top: 15px; vertical-align: middle; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;'>
        <table class='heading_block block-1' width='100%' border='0' cellpadding='0' cellspacing='0' role='presentation' style='mso-table-lspace: 0pt; mso-table-rspace: 0pt;'>
            <tr>
                <td class='pad' style='padding-bottom:5px;padding-left:10px;padding-right:10px;padding-top:5px;text-align:center;width:100%;'>
                    <h1 style='margin: 0; color: #012970; direction: ltr; font-family: 'Noto Serif', Georgia, serif; font-size: 24px; font-weight: 700; letter-spacing: normal; line-height: 180%; text-align: center; margin-top: 0; margin-bottom: 0;'><span class='tinyMce-placeholder'>&nbsp;<br></span></h1>
                </td>
            </tr>
        </table>
        <table class='heading_block block-2' width='100%' border='0' cellpadding='0' cellspacing='0' role='presentation' style='mso-table-lspace: 0pt; mso-table-rspace: 0pt;'>
            <tr>
                <td class='pad' style='padding-bottom:5px;padding-left:10px;padding-right:10px;padding-top:5px;text-align:center;width:100%;'>
                    <h1 style='margin: 0; color: #201f42; direction: ltr; font-family: Inter, sans-serif; font-size: 16px; font-weight: 400; letter-spacing: normal; line-height: 120%; text-align: left; margin-top: 0; margin-bottom: 0;'><span class='tinyMce-placeholder'>Email:&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;info@gemmaretail.com</span></h1>
                </td>
            </tr>
        </table>
        <table class='paragraph_block block-3' width='100%' border='0' cellpadding='10' cellspacing='0' role='presentation' style='mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;'>
            <tr>
                <td class='pad'>
                    <div style='color:#201f42;direction:ltr;font-family:Inter, sans-serif;font-size:17px;font-weight:400;letter-spacing:0px;line-height:180%;text-align:left;mso-line-height-alt:30.6px;'>
                        <p style='margin: 0;'>Phone:&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;03259606206</p>
                    </div>
                </td>
            </tr>
        </table>
    </td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table>
<table class='row row-7' align='center' width='100%' border='0' cellpadding='0' cellspacing='0' role='presentation' style='mso-table-lspace: 0pt; mso-table-rspace: 0pt;'>
<tbody>
<tr>
<td>
<table class='row-content stack' align='center' border='0' cellpadding='0' cellspacing='0' role='presentation' style='mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 700px;' width='700'>

</table>
</td>
</tr>
</tbody>
</table>
</td>
</tr>
</tbody>
</table><!-- End -->
</body>

</html>";
                    $mail = new PHPMailer();
                    //Set mailer to use smtp
                    $mail->isSMTP();
                    //Define smtp host
                    $mail->Host = "smtp.gmail.com";
                    //Enable smtp authentication
                    $mail->SMTPAuth = true;
                    //Set smtp encryption type (ssl/tls)
                    $mail->SMTPSecure = "tls";
                    //Port to connect smtp
                    $mail->Port = "587";
                    //Set gmail username
                    $mail->Username = "hitechcoder.6at@gmail.com";
                    //Set gmail password
                    $mail->Password = "arztydqludqarwig";
                    //Email subject wzkb plnw oglu vcmd
                    $mail->Subject = $subject;
                    //Set sender email
                    $mail->setFrom('hitechcoder.6at@gmail.com', 'Info');
                    //Enable HTML
                    $mail->isHTML(true);

                    $mail->Body = $html1 . $subject . $html2 . $message . $html3;
                    //Add recipient
                    $mail->addAddress($email);
                    //Finally send email
                    if ($mail->send()) {
                        $message = "Email Sent..!";
                    } else {
                        $message = "Message could not be sent. Mailer Error: ";
                    }
                    //Closing smtp connection
                    $mail->smtpClose();
                }

                if (!empty($message)) { ?>
                    <div class="success alert alert-success alert-dismissible fade show">
                        <strong>
                            <?php echo $message; ?>
                        </strong>
                    </div>
                <?php } ?>
            </form>
        </div>
    </section>




</body>

</html>