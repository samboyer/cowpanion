<?php
// ----------------------------------------------------------------------------
// webhook.php - Cowpanion message webhook handler
//
// November 2022, Sam Boyer
// ----------------------------------------------------------------------------

ini_set('error_reporting', E_ALL);

// Imports
foreach (glob("CowSay/src/Traits/*.php") as $filename) require_once($filename);
foreach (glob("CowSay/src/Core/*.php") as $filename) require_once($filename);
require_once("CowSay/src/Carcases/Cow.php");
use CowSay\Cow;


// == Config ==
$DEBUG_RECIPIENT = 'saboyer@cisco.com';

$COWPANION_KEY = file_get_contents("BOT_KEY");
$COWPANION_ID = 'Y2lzY29zcGFyazovL3VzL1BFT1BMRS81ZjkzZDg5Yy02YWJkLTQ3NWYtOTU3ZS01NTc3ZTBkNDc2MTc';


//  == Consts ==
$USAGE = "Usage:
- [cowpanion] say your_message
  - Cow says your_message to you.
- [cowpanion] send recipient_email_address your_message
  - Cow says your_message to the given recipient.
";


// == Debug functions ==

function send_debug_message($message_body_markdown) {
    GLOBAL $DEBUG_RECIPIENT;
    return send_message($DEBUG_RECIPIENT, $message_body_markdown);
}

function debug_log_message_info($msg_info) {
    $sender_email = $msg_info->{'personEmail'};
    $msg_text = $msg_info->{'text'};
    $msg_ts = $msg_info->{'created'};
    $dbg_msg = "[DEBUG] $sender_email ($msg_ts): $msg_text\n";

    send_debug_message($dbg_msg);

    $fp = fopen('webhook.log','a');
    fwrite($fp, $dbg_msg);
    fclose($fp);
}



// == Helper functions ==



//  == Message send/recv ==
function send_message($recipient, $message_body_markdown) {
    GLOBAL $COWPANION_KEY;

    assert(!is_null($message_body_markdown), "empty message");

    $url = 'https://webexapis.com/v1/messages';

    $data = array(
        'toPersonEmail' => $recipient,
        'markdown' => $message_body_markdown
    );

    $headers = array(
        "Authorization: Bearer $COWPANION_KEY",
        // 'Content-Type: multipart/form-data'
    );

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    $curl_response = curl_exec($ch);
    curl_close($ch);

    return json_decode($curl_response);
}

function get_message_info($message_id) {
    GLOBAL $COWPANION_KEY;

    $url = "https://webexapis.com/v1/messages/$message_id";


    $headers = array(
        "Authorization: Bearer $COWPANION_KEY",
    );

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    $curl_response = curl_exec($ch);
    curl_close($ch);

    return json_decode($curl_response);

}

function send_cow_message($recipient, $cowsay_input) {
    $cow_obj = new Cow($cowsay_input);
    $cow_out = $cow_obj->say();
    $response = "```\n$cow_out\n```";

    return send_message($recipient, $response);
}

function send_usage($recipient, $error_string) {
    GLOBAL $USAGE;
    if ($error_string !== "") {
        $msg = "$error_string\n$USAGE";
    } else {
        $msg = $USAGE;
    }

    return send_cow_message($recipient, $msg);
}

function send_error($recipient, $error_string) {
    return send_cow_message($recipient, $error_string);
}

function send_hint($recipient) {
    $cow_obj = new Cow('mooooooooo');
    $cow_out = $cow_obj->say();
    $response = "```\n$cow_out\n(Send 'help' to see commands)\n```";

    return send_message($recipient, $response);
}


// test
// $resp = send_message("this_email_doesnt_exist@samboyer.uk", 'hello');
// if (property_exists($resp, 'errors') && count($resp->{'errors'}) > 0) {
//     echo "error found\n";
//     echo $resp->{'errors'}[0]->{'description'};
// }
// exit();

// $re_mention = '/<spark-mention data-object-type="\w+" data-object-id="(\w+)">[^<]+<\/spark-mention>\s*/'




// == Main path ==
$notif_body = json_decode(file_get_contents('php://input'));

$sender_email = $notif_body->{'data'}->{'personEmail'};
if ($sender_email == 'cowpanion@webex.bot') {
    exit();
}

$msg_info = get_message_info($notif_body->{'data'}->{'id'});
debug_log_message_info($msg_info);

$is_dm = ($msg_info->{'roomType'} === 'direct');

$msg_text = $msg_info->{'text'};

$msg_words = explode(' ',
str_replace("\n", ' ',
preg_replace('/ +/',' ', $msg_text)
)
);


// If the first word is a tag of the bot, strip it
$bot_mentioned = false;
foreach ($msg_info->{'mentionedPeople'} as $person_id) {
    if ($person_id === $COWPANION_ID) {
        $bot_mentioned = true;
    }
}

if ($bot_mentioned && !$is_dm && $msg_words[0] == 'cowpanion') {
    $msg_words = array_slice($msg_words, 1);
}

// Main command handling
if ($bot_mentioned || $is_dm) {
    if ($msg_words[0] === 'say') {
        $message_to_say = preg_replace(
            '/\s*say\s+/',
            '',
            $msg_text,
            1
        );
        send_cow_message($sender_email, $message_to_say);
    }
    elseif ($msg_words[0] === 'send') {
        $cmd_send_recipient = $msg_words[1];


        if (preg_match('/^[\w_.+-]+@[\w-]+\.[\w-.]+$/', $cmd_send_recipient) == 1) {
            $message_to_say = preg_replace(
                '/\s*send\s+[^\s]+\s+/',
                '',
                $msg_text,
                1
            );

            $resp = send_cow_message($cmd_send_recipient, $message_to_say);

            if (property_exists($resp, 'errors')
                && count($resp->{'errors'}) > 0) {
                // If sending message fails, report an error to the user.
                send_message($sender_email, "Error: "
                    . $resp->{'errors'}[0]->{'description'});
            }
            else{
                send_message($sender_email, "Sent!");
            }
        }
        else {
            send_usage($sender_email, "Invalid recipient $cmd_send_recipient");
        }
    }
    elseif ($msg_words[0] === 'help') {
        send_usage($sender_email, '');
    }
    else {
        send_hint($sender_email);
    }

}
else {
    send_hint($sender_email);
}



/*
expected flow (v1)

if cowpanion isn't mentioned, send default message to sender ('moo')

if cowpanion is mentioned,
    if first word is 'say',
        echo rest of message within cow
    elif first word is 'send',
        if second word is an email address,
            echo rest of message within cow to recipient
            if message fails to send,
                send_error($sender_email, "Failed to send: %s");
        else send_usage($sender_email, "Invalid recipient");

    else echo usage (within a cow)

==v2==

if cowpanion isn't mentioned, put whole message through eliza, echo cow response


*/
?>