#!/usr/local/bin/perl 
local our $VERSION = '2.7';
use DBI;
use Custom::Date;
use Custom::MB::Usergroup; # Implement usergroup version 2.0 and latter it override orignal usergroup module
use Custom::Toolbar;
use Custom::Global;
require '/www/htdocs/cgi/subs.cgi';
require '/www/htdocs/cgi/tools/include.cgi';
require '/www/htdocs/cgi/members/pass.cgi';

#use CGI;
#$req = new CGI;
#%FORM = $req->Vars;
#local our $certificate_filepath = $req->param("certificate"); # for user certificate upload.
#local our $metadata_filepath = $req->param("usermetadata"); # for user metadata upload.
#local our ($certificate_exist,$metadata_exist);
#require LWP::UserAgent;

our (%global,%settings,%FORM,%DB);
&getinfo;
&checkpass();
END {
    #undefined all the Local Global and Shared Local Global variables here. 
	Custom::MB::Usergroup::destroy();
	Custom::Toolbar::destroy();
	Custom::Global::destroy();
}

$DB{mb} = dbConnect("mb");
$global{uid}= $uid;

# subroutine calling according to action.
if ($FORM{action} eq "updatemb") {&updatemb;}
if ($FORM{action} eq "showmbsettings") {&showmbsettings;}
if ($FORM{action} eq "deletecertificate") {&delte_doc;}
if ($FORM{action} eq "deletemetadata") {&delte_metadata;}
if ($FORM{action} eq "download") {&download_certificate;}
if ($FORM{action} eq "downloadmetadata") {&download_metadata;}
if ($FORM{action} eq "generateapikey") {&generateApiKey;}
&doError("Error: Action not found" , "1");
#########################################################
sub showmbsettings {

if ($FORM{already}) {
	($found) = $DB{mb} -> selectrow_array("SELECT uid FROM settings WHERE uid='$uid'");
} else {
	($found, $FORM{title}, $FORM{perpage}, $FORM{replies}, $FORM{slb}, $FORM{display_icons}, $FORM{pass}, $FORM{flood}, $FORM{vulgarity_lvl}, $FORM{htmlblock}, $FORM{notify}, $FORM{notifyreply}, $FORM{smilie}, $FORM{easycode}, $FORM{timeoffset}, $FORM{dst}, $FORM{display_time}, $FORM{reqreg}, $FORM{reqregapp}, $FORM{notifyreg}, $FORM{confirm_email}, $FORM{show_num_users}, $FORM{allow_pm}, $FORM{av_width}, $FORM{av_height}, $FORM{mod_display}, $FORM{enable_spellcheck}, $FORM{uses_forums}, $FORM{wysiwyg}, $FORM{allow_emails}, $FORM{allow_subscribe}, $FORM{allowmultiregs}, $FORM{use_captcha},$FORM{use_captcha_registration}, $FORM{sitename}, $FORM{siteurl}, $FORM{date_format}, $FORM{allowthreadreview}, $FORM{allow_forum_subscribe}, $FORM{enable_rssfeed}, $FORM{allow_rss_feed}, $FORM{chat_link}, $FORM{active_chat_users}, $FORM{enable_chat_bar}, $FORM{views_col}, $FORM{subdomain_url}, $FORM{enable_calendar}, $FORM{system_email}, $FORM{upcoming_events}, $FORM{enable_polls}, $FORM{maximum_poll_options}, $FORM{update_lastpost_on_pollvote}, $FORM{display_birthday}, $FORM{online_user_list}, $FORM{online_user_statistic}, $FORM{body_page_title}, $FORM{new_user_registration}, $FORM{enable_social_bookmarking},$FORM{word_wrap},$FORM{quick_reply},$FORM{idp_login_url},$FORM{customer_logout_request_listener_url},$FORM{customer_logout_response_listener_url},$FORM{logout_page_url},$FORM{registration_url}, $FORM{login_page_url}, $FORM{username_regexp},$FORM{sso_enabled},$FORM{allow_two_way_sso}, $FORM{apikey}, $FORM{show_private_forums},$FORM{file_uploading},$FORM{avatar_uploading},$FORM{profile_picture},$FORM{max_file_size},$FORM{reqreg},$FORM{file_types},$avatarwidth,$FORM{notification_preference},$FORM{attachment_display},$FORM{logo},$FORM{forum_rules},$FORM{enable_albums}) = 
	$DB{mb} -> selectrow_array("SELECT uid, title, threadsperpage, repliesperpage, showlinkback, displayicons, protectionpw, flood, profanitylvl, htmlfilter, notifythread, notifyreply, enablesmilies, enableeasycode, timeoffset, dst, displaytime, reqreg, reqregapp, notifyreg, confirmemail, shownumusers, allowpm, avatarwidth, avatarheight, moddisplay, spellcheck, uses_forums, wysiwyg, allow_emails, allow_subscribe, allowmultiregs, use_captcha, use_captcha_registration,sitename, siteurl, dateformat, threadreview, allow_forumsubscribe, enable_rssfeed, rssfeed, chat_link, active_chat_users, enable_chat_bar, allow_views_column, subdomain_url, enable_calendar, system_email, upcoming_events, enable_polls, maximum_poll_options, update_lastpost_on_pollvote, display_birthday, online_user_list, online_user_statistic, body_page_title, new_user_registration, enable_social_bookmarking,word_wrap, quick_reply, idp_login_url, customer_logout_request_listener_url, customer_logout_response_listener_url, logout_page_url, registration_url, login_page_url, username_regexp,sso_enabled,allow_two_way_sso, apikey, show_private_forums, file_uploading, avatar_uploading, profile_picture, max_file_size, reqreg,file_types, avatarwidth, notification_preference, attachment_display,logo,forum_rules,enable_albums FROM settings WHERE uid='$uid'");
}

##### set up the moderator display checkboxes
if ($FORM{mod_display} =~ /desc/) {
	$CHECKED{desc} = "checked";
}

if ($FORM{mod_display} =~ /footer/) {
	$CHECKED{footer} = "checked";
}

if ($FORM{mod_display} =~ /column/) {
	$CHECKED{column} = "checked";
}
##### end set up checkboxes

##### set up the post icons display checkboxes
if ($FORM{display_icons} =~ /im/) {
	$CHECKED{im} = "checked";
}

if ($FORM{display_icons} =~ /quote/) {
	$CHECKED{quote} = "checked";
}
##### end set up checkboxes

# so that you don't get locked out of the textbox
$FORM{title} =~ s/"/&quot;/g;

$DATE_FORMAT{$FORM{date_format}} = "selected";
$TIME_FORMAT{$FORM{display_time}} = "selected";
$FILTER{$FORM{vulgarity_lvl}} = "selected";
$EDITOR{$FORM{wysiwyg}} = "selected";

# if polls are ebable show set the variable property to display the DIV element
my $display_poll_settings = $FORM{enable_polls} ? "block" : "none";

# File uploading settings
$reg_disable = "disabled" if (!$FORM{reqreg} || $avatarwidth eq "NA");

$SELECTED{$FORM{notification_preference}} = "selected";
$SELECTED{$FORM{attachment_display}} = "selected";

$max_file_size_human = type($FORM{max_file_size} * 1024);

# show the message
if ($_[0]) {
	$err = qq~<br><br><div style="width:90%; text-align:left; margin: auto; color: red;" class="heading">$_[0]</div>~;
}

print "Content-type: text/html\n\n";

if (!$found) {
	&toolstop("m");
} else {
	&toolstop("m", "mb");
}
# we are checking hear wheather the client has uploaded the certificate if the certificate is already uploaded we are not showing upload certificate button.

# The path of certificate where user's certificate is uploaded
my $certificate_path = "/usr/local/etc/chat_bar/certs/";

# We are opening the directory and checking wheather the file with exact user name is existing or not.
my @files;
opendir(DIR, $certificate_path);
@files = readdir(DIR);
close(DIR);

my $certificate = grep /^$FORM{username}\./, @files;
# We are assigning the value in the $certificate variable wheather the certificate file exist in the $certificate path.
# if the certificate exist we are assigning $certificate =1, by this way we are hiding the upload certifcate button in SAML GUI and showing the delete certificate link.
if($certificate){
	$certificate_exist=1;
}
# End of certificate check.
# we are checking hear wheather the client has uploaded the metadata if the metadata is already uploaded we are not showing upload metadata button.

# The path of metadata where user's metadata is uploaded
my $meta_data_path = "/usr/local/etc/chat_bar/metadata/";

# We are opening the directory and checking wheather the file with exact user name is existing or not.
my @meta_files;
opendir(METADIR, $meta_data_path);
@meta_files = readdir(METADIR);
close(METADIR);

my $metadata = grep /^$FORM{username}\./, @meta_files;
# We are assigning the value in the $metadata variable wheather the metadata file exist in the $meta_data_path.
# if the metadata exist we are assigning $metadata_exist =1, by this way we are hiding the upload certifcate button in SAML GUI and showing the delete certificate link.
if($metadata){
	$metadata_exist=1;
}
################# End of metadata check.
my $tab_id = 1;

#Make the tab directly opened through URL active
#Assign tab_id to track last selected tab 
if (lc($FORM{tab}) eq 'general') {
	$tab_id = 2;
} elsif (lc($FORM{tab}) eq 'security') {
	$tab_id = 3;
} elsif (lc($FORM{tab}) eq 'notification') {
	$tab_id = 4;
} elsif (lc($FORM{tab}) eq 'time') {
	$tab_id = 5;
} elsif (lc($FORM{tab}) eq 'chat') {
	$tab_id = 6;
} elsif (lc($FORM{tab}) eq 'single sign on') {
	$tab_id = 7;
} elsif (lc($FORM{tab}) eq 'file uploading') {
	$tab_id = 8;
}

# Check if Logo is uploaded
my $logo_id;
if ($FORM{logo}) {
	$logo_id = $DB{mb} -> selectrow_array("SELECT fileid FROM attachment WHERE uid='$global{uid}' AND fileid='$FORM{logo}' AND type='3'") ;
}
# Set display style for Logo Upload options
# $action_change tells the action of upload logo feature.
# action_change = 0 => Logo not uploaded, Display "Upload a logo from your computer" link
# action_change = 1 => user clicked "Change" link, hence delete logo and upload a new one. Also display "View|Change|Delete" Link 
# When a user clicks "delete", there is no role of action_change
my ($action_change,$uploadedLogoStyle) ;
if ($logo_id) {
	$action_change = "1";
	$uploadedLogoStyle = '';
}
else {
	$uploadedLogoStyle = "style=\"display:none\"";
}
# Define all variables required for logo upload before general_settings.js is loaded else they remain undefined in ready function.
print qq~
<script type="text/javascript"> 
	var action_change = '$action_change';
	var logo = '$logo_id';
	var uid = '$global{uid}';
	\$(function() {
		\$('#gallery a').lightBox({imageBtnClose:'/images/js/lightbox/cancel.png'});
	});
</script>
<script type="text/javascript" src="/js/tabs.js?v1.00"></script>
<script type="text/javascript" src="/js/mb/general_settings.js?v1.03"></script>
<script language="JavaScript">
	var sel_tab = $tab_id;
</script>
<style>
#slider, #slider1, #slider2, #slider3{
	display: inline-block;
	width: 162px;
}
#slider_values, #slider_values1, #slider_values2, #slider_values3{
	display: inline-block;
}
</style>
<!--  <form name="posts" method="post" enctype="multipart/form-data" action="/cgi/members/mboard.cgi" onSubmit="return checkForm()">-->
  <form name="posts" method="post" action="/cgi/members/mboard.cgi" onSubmit="return checkForm()">
	<div><center>
		<span class="heading" >Forum Settings</span></center>
		$err
		
		<div><br><br></div>
	</div> 

	<div id="tab_wrapper">
		<div id="content">
			<div class="tab_menu">
				<ul>
					<li id="tab1">
						<a href="#" onclick="show_next_tab('tab1', 0, 0 ); return false;"><span class="tab" title="Display">Display</span></a>
					</li>
		
					<li id="tab2">
						<a href="#" onclick="show_next_tab('tab2', 1, 0); return false;"><span class="tab" title="General">General</span></a>
					</li>
		
					<li id="tab3">
						<a href="#" onclick="show_next_tab('tab3', 2, 0 ); return false;"><span class="tab" title="Security">Security</span></a>
					</li>
		
					<li id="tab4">
						<a href="#" onclick="show_next_tab('tab4', 3, 0 ); return false;"><span class="tab" title="Notification">Notification</span></a>
					</li>
		
					<li id="tab5">
						<a href="#" onclick="show_next_tab('tab5', 4, 0); return false;"><span class="tab" title="Time">Time</span></a>
					</li>
		
					<li id="tab6">
						<a href="#" onclick="show_next_tab('tab6', 5, 0 ); return false;"><span class="tab" title="Chat">Chat</span></a>
					</li>
		
					<li id="tab7">
						<a href="#" onclick="show_next_tab('tab7', 6, 0 ); return false;"><span class="tab" title="Single Sign On">Single Sign On</span></a>
					</li>
					<li id="tab8">
						<a href="#" onclick="show_next_tab('tab8', 7, 0); return false;"><span class="tab" title="File Uploading">File Uploading</span></a>
					</li>
				</ul>
			</div>
		~;

print qq~<script>document.write('<div class="box" style="display:none"><h1></h1>')</script>
		<noscript><div class="box" style="display:block"><h1></h1></noscript>
	<!-- Begin Display Options -->
	<table width="490" border="0" cellspacing="0" cellpadding="6" class=text>
	<noscript>
	<tr>
		<td colspan="2" class="heading">Display Settings:</td>
	</tr>
	</noscript>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)"> 
		<td>Forum title:</td>
		<td><input type="text" name="title" value="$FORM{title}" maxlength=250 size=25></td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)"> 
		<td><span onclick="toggleTooltip('','Display the title on the body of the page', this);" class="help_tooltip_img" title="Help"></span> Display the title on the body of the page:</td>
		<td><input type="checkbox" name="body_page_title" value="checked" id="body_page_title" $FORM{body_page_title}><label for="body_page_title" title="Display the title on the body of the page" style="cursor:pointer"> Yes </label></td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
		<td nowrap><span onclick="toggleTooltip('','Add a business logo (header image) to display at the top of all your forum pages.', this);" class="help_tooltip_img" title="Help"></span> Logo:</td>
		<td nowrap>
		<!-- code for upload, view ,change and delete option for logo -->
			<div id="uploadLogo" >
			<span id="gallery" $uploadedLogoStyle><a id="viewLogo" href="http://files.websitetoolbox.com/$global{uid}/$logo_id" target="_blank">View</a> | </span>
			<a href="#" id="attachLogo">Upload a logo from your computer</a>
			<span id="deletelogo" $uploadedLogoStyle> | <a href="#" id="deleteLogo" onclick="deleteLogo(document.posts.logo.value,$global{uid}); return false;">Delete</a></span>
			</div>
			<div id="logoStatus"></div>
			<!-- Load plupload and all it's runtimes -->
			<script type="text/javascript" src="/js/mb/plupload.full.js"></script>
			<script type="text/javascript" src="/js/mb/jquery.lightbox-0.5.js"></script>
			<link rel="stylesheet" type="text/css" href="/tools/jquery.lightbox-0.5.css" media="screen" />
			</td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
		<td nowrap><span onClick="toggleTooltip('','Enabling this option will cause a link to your website to be displayed in the navigation area of the forum. The name and address for your website should be specified in the corresponding options shown below.', this);" class="help_tooltip_img" title="Help"></span> Add a link back to your site:</td>
		<td><input type="checkbox" name="slb" value="checked" id="SLBY" onClick="return checkSiteName(this);" $FORM{slb}><label for="SLBY" title="Add link" style="cursor:pointer"> Yes </label></td>
	</tr>
	<tbody  id="link_back" style="display:none;">
		<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
			<td nowrap><span onclick="toggleTooltip('','Your website name will be used to create a return link in your forum so that your visitors can go back to your website. The return link feature can easily be turned off through the setting below.<p>If you do not have a website, simply leave this field blank.</p>', this);" class="help_tooltip_img" title="Help"></span> Your website name:</td>
			<td><input type="text" name="sitename" value="$FORM{sitename}" maxlength=50 tabindex=12 size=25></td>
		</tr>
		<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
			<td nowrap><span onclick="toggleTooltip('','Your website URL will be used to create a return link in your forum so that your visitors can go back to your website if the <i>Add a link back to your site</i> option is enabled.<p>If you do not have a website URL, simply leave this field blank.', this);" class="help_tooltip_img" title="Help"></span> Your website address:</td>
			<td nowrap><input type="text" name="siteurl" value="$FORM{siteurl}" maxlength=200 tabindex=13 size=25> &nbsp;<a href="#" onClick="testURL(document.posts.siteurl.value); return false;"><img src="/images/view.gif" width="14" height="16" border="0" alt="Preview the URL" style="vertical-align: middle;"></a></td>
		</tr>
	</tbody>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)"> 
		<td nowrap><span onClick="toggleTooltip('','This is the default number of topics that will be listed on each page when viewing a forum. ', this);" class="help_tooltip_img" title="Help"></span> Default topics to display per page:</td>
		<td nowrap>
			<div id="slider_options1"><input type="text" name="perpage" id="perpage" value="$FORM{perpage}" size=3 maxlength=3></div><div id="slider1" class="ui-slider ui-slider-horizontal ui-widget ui-widget-content ui-corner-all"><a href="#" class="ui-slider-handle ui-state-default ui-corner-all"></a></div>&nbsp;&nbsp; <span id="slider_values1">$FORM{perpage} Topics</span>
		</td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)"> 
		<td nowrap><span onClick="toggleTooltip('','This is the default number of replies/posts that will be listed on each page when viewing a topic.', this);" class="help_tooltip_img" title="Help"></span> Default replies to display per page:</td>
		<td nowrap>
			<div id="slider_options2"><input type="text" name="replies" id="replies" value="$FORM{replies}" size=3 maxlength=3></div><div id="slider2" class="ui-slider ui-slider-horizontal ui-widget ui-widget-content ui-corner-all"><a href="#" class="ui-slider-handle ui-state-default ui-corner-all"></a></div>&nbsp;&nbsp; <span id="slider_values2">$FORM{replies} Replies</span>
		</td>
	</tr>
	<tr onmouseover="mOvr(this);" onmouseout="mOut(this);" >
		<td nowrap><span onclick="toggleTooltip('','Enabling this option will cause the Display forthcoming events option appear automatically on main forum page. This option is enable only if Enable Calendar option is enable.', this);" class="help_tooltip_img" title="Help"></span> Days to display upcoming events from:</td>
	
		<td nowrap>
			<div id="slider_options3"><input type="text" name="upcoming_events" id="upcoming_events" value="$FORM{upcoming_events}" size=3 maxlength=3></div><div id="slider3" class="ui-slider ui-slider-horizontal ui-widget ui-widget-content ui-corner-all"><a href="#" class="ui-slider-handle ui-state-default ui-corner-all"></a></div>&nbsp;&nbsp; <span id="slider_values3"></span>
		</td>
	</tr>
	<tr onmouseover="mOvr(this); showTip('word_wrap_tip');" onmouseout="mOut(this); hideTip('word_wrap_tip');">
		<td><span onclick="toggleTooltip('','If you want posts to automatically insert spaces into long words to make them wrap after a certain number of characters, set the number of characters in the provided textbox. A common choice for word wrapping is 50 characters.<p>Enter 0 to disable word wrapping.', this);" class="help_tooltip_img" title="Help"></span> Number of characters before wrapping text:</td>
		<td nowrap>
		<input type="text" name="word_wrap" value="$FORM{word_wrap}" maxlength="3" size="3">
		&nbsp;<span id="word_wrap_tip" style="display: none;"><img src="/images/note.gif" alt="Tip" height="13" width="15"> Tip: Enter 0 to disable</span>
		</td>
	</tr>
	<tr onmouseover="mOvr(this); showTip('av_tip');" onmouseout="mOut(this); hideTip('av_tip');"> 
		<td nowrap><span onclick="toggleTooltip('Avatar','An avatar is a small image that is displayed under the username in a member\\'s post and in their profile. It is an optional feature that members generally enjoy.', this);" class="help_tooltip_img" title="Help"></span> Avatar size:</td>
		<td nowrap>
		Width: &nbsp;<input type="text" name="av_width" value="$FORM{av_width}" size=3 maxlength=3><br>
		Height: <input type="text" name="av_height" value="$FORM{av_height}" size=3 maxlength=3>
		&nbsp;<span id="av_tip" style="display: none;"><img src="/images/note.gif" alt="Tip" height="13" width="15"> Tip: Enter 'NA' to disable</span>
		</td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
		<td><span onclick="toggleTooltip('','This option specifies what icons will appear in a post. The \\'Quote\\' icon allows a user to post a reply to a topic while quoting a previously posted reply. The \\'Instant Messenger\\' icon allows a user to contact the author of the post through an external chat program on their computer.', this);" class="help_tooltip_img" title="Help"></span> Icons to display in posts:</td>
		<td>
<!-- ATTN: if new option added, edit printing to DB -->
		<input type="checkbox" name="display_icons3" value="quote" id="diQuote" $CHECKED{quote}><label for="diQuote" title="Display the quote icon" style="cursor:pointer"> Quote </label><br>
		<input type="checkbox" name="display_icons4" value="im" id="diIM" $CHECKED{im}><label for="diIM" title="Display the instant messenger icon" style="cursor:pointer"> Instant messenger </label><br></td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)"> 
		<td nowrap><span onclick="toggleTooltip('Forum moderator display','This option allows you to choose where to list the moderators that are assigned to a forum.<p>Note: Moderators with permission to \\'All Forums\\' are not listed in the selected areas. Only moderators that are assigned to specific forums are listed.', this);" class="help_tooltip_img" title="Help"></span> Forum moderator display:</td>
		<td><input type="checkbox" name="mod_display" value="column" id="mdColumn" $CHECKED{column}><label for="mdColumn" title="Displayed as a separate column in the forum listing" style="cursor:pointer"> In separate column </label><br><input type="checkbox" name="mod_display2" value="desc" id="mdFD" $CHECKED{desc}><label for="mdFD" title="Displayed with the forum description in the forum listing" style="cursor:pointer"> In forum description </label><br><input type="checkbox" name="mod_display3" value="footer" id="mdfooter" $CHECKED{footer}><label for="mdfooter" title="Displayed at the bottom of the forum page" style="cursor:pointer"> Forum page </label></td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)"> 
		<td nowrap><span onClick="toggleTooltip('','Enabling this option will cause the text \\'Members: X\\' (where X is the number of user accounts in your forum) to be displayed at the bottom of the main page of your forum. A link to a list of all registered user accounts will also be displayed.', this);" class="help_tooltip_img" title="Help"></span> Show number of members registered and members list:&nbsp;</td>
		<td><input type="checkbox" name="show_num_users" value="checked" id="s_num_users" $FORM{show_num_users}><label for="s_num_users" title="Show number of users" style="cursor:pointer"> Yes </label></td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)"> 
		<td><span onclick="toggleTooltip('','Enable this option to display today\\'s birthday\\'s on forum homepage.', this);" class="help_tooltip_img" title="Help"></span> Display today's birthdays:</td>
		<td><input type="checkbox" name="display_birthday" value="checked" id="display_birthday" $FORM{display_birthday}><label for="display_birthday" title="Display today's birthdays" style="cursor:pointer"> Yes </label></td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)"> 
		<td><span onclick="toggleTooltip('','The online users list is a comma-separated list of users that are currently browsing your forum. Enabling this option will cause the online users list to be displayed at the bottom of the main page of your forum.', this);" class="help_tooltip_img" title="Help"></span>
		Show online users list:</td>
		<td><input type="checkbox" name="online_user_list" value="checked" id="online_user_list" $FORM{online_user_list}><label for="online_user_list" title="Show online users list" style="cursor:pointer"> Yes </label></td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)"> 
		<td><span onClick="toggleTooltip('','The <i>most users ever online</i> statistic is a number representing the maximum number of users that have ever browsed your forum at once. It is essentially the maximum number of users that have ever been displayed on the online user list at one time. Enabling this option will display the statistic at the bottom of the main page of your forum.', this);" class="help_tooltip_img" title="Help"></span> Show "most users ever online" statistic:</td>
		<td><input type="checkbox" name="online_user_statistic" value="checked" id="online_user_statistic" $FORM{online_user_statistic}><label for="online_user_statistic" title="Show most users ever online statistic" style="cursor:pointer"> Yes </label></td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
		<td><span onclick="toggleTooltip('','Enabling this option will cause the views column to appear on topics listing page. You can disable this option if you do not want users to know how many times a topic has been viewed.', this);" class="help_tooltip_img" title="Help"></span> Display the "Views" column in the topics list:
		</td>
		<td><input type="checkbox" name="views_col" value="checked" id="vwCOL" $FORM{views_col}><label for="vwCOL" style="cursor:pointer"> Yes </label></td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
		<td><span onclick="toggleTooltip('','Enabling this option will allow users to see all forums that they don\\'t have access to.<p>Disabling this option will hide private forums from users who are not allowed to access them. Users who do have permission to access them will have to log in before they can see these forums too.', this);" class="help_tooltip_img" title="Help"></span> Show private forums:
		</td>
		<td><input type="checkbox" name="show_private_forums" value="checked" id="show_private_forumsCOL" $FORM{show_private_forums}><label for="show_private_forumsCOL" style="cursor:pointer"> Yes </label></td>
	</tr>
	<!-- End Display Options -->
	<!-- Begin Code Options -->
	<tr><td colspan="2"><br></td></tr>
	<tr>
		<td colspan="2" class="heading">Code Settings:</td>
	</tr>
	<tr onmouseover="mOvr(this); showTip('smilie_tip');" onmouseout="mOut(this); hideTip('smilie_tip');">
		<td nowrap><span onclick="toggleTooltip('Graphical Smilies','Enabling this option will allow users to post small graphical images that you have specified.<p>Click the <i>View Smilies</i> link to view the smilies that are currently available for use on your forum. Click the <i>Add Smilies</i> link to add additional smilies to your forum.', this);" class="help_tooltip_img" title="Help"></span> Enable graphical smilies: </td>
		<td style="height: 27px;" nowrap>
		<input type="checkbox" name="smilie" value="checked" id="SMSH" $FORM{smilie}><label for="SMSH" title="Enable smilies" style="cursor:pointer"> Yes </label>
		&nbsp;&nbsp;&nbsp;<span id="smilie_tip" style="display: none;"><a href="#" id="smilie_dialog"><span class="button" style="vertical-align: middle;">View Smilies</span></a> 
		<a href="/tool/members/smilies?tool=mb" onClick="return confirmExit();"><span class="button" style="vertical-align: middle;">Add Smilies</span></a></span>
		</td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
		<td nowrap><a name=easycode></a><span onclick="toggleTooltip('EasyCode','EasyCode allows your forum users to post advanced messages without knowing html. It will allow them to post bold, italicized, and underlined text, links, email links, images, quotes, and visible code by pressing the corresponding button on the <i>Post a new message</i> page.', this);" class="help_tooltip_img" title="Help"></span> Enable EasyCode:</td>
		<td><input type="checkbox" name="easycode" value="checked" id="ezcode" onClick="easycodeCheck();" $FORM{easycode}><label for="ezcode" title="Enable EasyCode" style="cursor:pointer"> Yes </label></td>
	</tr>
	<!-- End Code Options -->
	</table>
	</div>

	<script>document.write('<div class="box" style="display:none"><h1></h1>')</script>
	<noscript><div class="box" style="display:block"><h1></h1></noscript	
	<!-- Begin General Options -->
	<table width="490" border="0" cellspacing="0" cellpadding="6" class="text"> 
   <noscript>
	<tr>
		<td colspan="2" class="heading">General Settings:</td>
	</tr>
	</noscript>
    <tr onmouseover="mOvr(this)" onmouseout="mOut(this)"> 
        	<td nowrap><a name=reg></a><span onclick="toggleTooltip('Member Registration','Enabling this option will allow users to create an account on your forum. The account can be used to create their profile, save their preferences, save their topic and forum subscriptions, hold their private messages, and much, much more. Users can still post messages and perform many activities without logging into their account if the \\'Unregistered / Not Logged In\\' has been given those permissions.<p>Disabling this feature will allow users to post messages with just their name and/or email address. However, none of the features mentioned previously can be used.', this);" class="help_tooltip_img" title="Help"></span> Member registration:</td>
        	<td><input type="checkbox" name="reqreg" value="checked" id="REQreg" onClick="regcheck('1');" $FORM{reqreg}><label for="REQreg" title="Require registration" style="cursor:pointer"> Enable </label></td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)"> 
		<td nowrap><span onclick="toggleTooltip('Enable photo album','Enable photo album', this);" class="help_tooltip_img" title="Help"></span> Enable photo albums:</td>
		<td nowrap><input type="checkbox" name="enable_albums" value="checked" id="eqr" $FORM{enable_albums}><label for="eqr" title="Enable photo album" style="cursor:pointer"> Yes </label></td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)"> 
			<td nowrap><span onclick="toggleTooltip('Enable polls','If this option is enabled, the system will allow the users to add polls in forum topics.', this);" class="help_tooltip_img" title="Help"></span> Polls:</td>
			<td nowrap><input type="checkbox" name="enable_polls" value="checked" id="enable_polls" $FORM{enable_polls}><label for="enable_polls" title="Enable polls" style="cursor:pointer"> Enable </label></td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)"> 
		<td nowrap><a name=pm></a><span onclick="toggleTooltip('Private Messaging','Private messaging is a convenient way for your members to contact one another privately without disclosing their email address. It\\'s like an email system built right into your forum!', this);" class="help_tooltip_img" title="Help"></span> Private messaging:</td>
		<td nowrap><input type="checkbox" name="allow_pm" value="checked" id="aPM" $FORM{allow_pm}><label for="aPM" title="Allow private messaging" style="cursor:pointer"> Enable </label></td>
      </tr>
      <tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
		<td nowrap><span onclick="toggleTooltip('Spell Checker','If this feature is enabled, your messsage board users will be able to identify any mispellings in their message by clicking a Spell Check button.', this);" class="help_tooltip_img" title="Help"></span> Spell check:</td>
		<td nowrap><input type="checkbox" name="enable_spellcheck" value="checked" id="eSC" $FORM{enable_spellcheck}><label for="eSC" title="Enable spell check" style="cursor:pointer"> Enable </label></td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)"> 
		<td nowrap><span onclick="toggleTooltip('Topic Review','Enabling this option will allow your users to view the last few posts in a topic when posting a reply.', this);" class="help_tooltip_img" title="Help"></span> Topic review:</td>
		<td nowrap><input type="checkbox" name="allowthreadreview" value="checked" id="Rvth" $FORM{allowthreadreview}><label for="Rvth" title="Enable topic review" style="cursor:pointer"> Enable </label></td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
		<td nowrap><span onclick="toggleTooltip('Enable RSS feeds','Turning off this option will prevent users from accessing your RSS feed. This may be useful if you are receiving a large amount of pageviews from your RSS feed and you would like to reduce your pageview usage fees. This feature is not available for free forums.', this);" class="help_tooltip_img" title="Help"></span> RSS feeds:</td>
		<td nowrap><input type="checkbox" name="enable_rssfeed" value="checked" id="eRSSF" onClick="rssFeed('1');" $FORM{enable_rssfeed} ><label for="eRSSF" title="Enable RSS feeds" style="cursor:pointer"> Enable </label></td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
		<td nowrap><span onclick="toggleTooltip('Allow RSS feed browser integration','If this feature is enabled, browsers that support RSS feeds will display an icon that the user can click to easily subscribe to the RSS feed for your forum.', this);" class="help_tooltip_img" title="Help"></span> RSS feed browser integration:</td>
		<td nowrap><input type="checkbox" name="allow_rss_feed" value="checked" id="aRSSF" $FORM{allow_rss_feed} ><label for="aRSSF" title="Allow RSS feed browser integration" style="cursor:pointer"> Enable </label></td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)"> 
		<td nowrap><span onclick="toggleTooltip('Enable the calendar','Enabling this option will allow users to post their event.', this);" class="help_tooltip_img" title="Help"></span> Calendar:</td>
		<td nowrap><input type="checkbox" name="enable_calendar" value="checked" id="enable_calendar" onClick="enableCal('1');" $FORM{enable_calendar}><label for="enable_calendar" title="Enable Calendar" style="cursor:pointer"> Enable </label></td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)"> 
		<td nowrap><span onclick="toggleTooltip('Enable social sharing','Enable this option to allow your users to easily share topics on Facebook and Twitter. Small sharing icons will be displayed on the bottom-left of the topic page.<p>If you find that no social bookmarking links are being displayed in a topic, check the permissions for guests in that topic. The links will only be shown in guest-viewable topics.', this);" class="help_tooltip_img" title="Help"></span> Social sharing:</td>
		<td nowrap><input type="checkbox" name="enable_social_bookmarking" value="checked" id="esb" $FORM{enable_social_bookmarking}><label for="esb" title="Enable Social Bookmarking" style="cursor:pointer"> Enable </label></td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)"> 
		<td nowrap><span onclick="toggleTooltip('Enable quick reply','If you enable this option, a box will appear at the bottom of each topic page allowing a user to quickly reply to the current topic without loading the full \\'New Reply\\' page.', this);" class="help_tooltip_img" title="Help"></span> Quick reply:</td>
		<td nowrap><input type="checkbox" name="quick_reply" value="checked" id="eqr" $FORM{quick_reply}><label for="eqr" title="Enable Quick Reply" style="cursor:pointer"> Enable </label></td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)"> 
		<td nowrap><span onclick="toggleTooltip('Text editor','Regular Textbox - Choosing this option will display a regular textbox without any advanced capabilities.<p>Advanced editor - This option will display the WYSIWYG (What You See Is What You Get) editor to users who have a compatible browser.', this);" class="help_tooltip_img" title="Help"></span> Message editor:</td>
		<td nowrap>
		<select name="wysiwyg">
		<option value="regular" $EDITOR{regular}>Regular Textbox
		<option value="both" $EDITOR{both}>Advanced Editor
		</select>
		</td>
	</tr>
	<tr valign="top">
		<script language="javascript" type="text/javascript">
		function ShowRules()
		{
			jQuery('#rules_edit').hide();
			jQuery('#rules_show').show();
		}
		</script>
		<td nowrap=""><span onclick="toggleTooltip('Forum Terms & Rules','Please specify your Forum Terms & Rules here. The users need to comply with these rules during Registration.', this);" class="help_tooltip_img" title="Help"></span> Forum Terms & Rules:</td>
		<td nowrap>
			<div id="rules_edit"><a href="javascript:void(0);" onClick="return ShowRules();">Edit Terms & Rules</a></div>
			<div id="rules_show" style="display:none;">
			<textarea id="forum_rules" name="forum_rules" class="mceEditor" cols="23" rows="1" wrap="virtual" tabindex='' tindex='' firstfocus="firstfocus">$FORM{forum_rules}</textarea><br>
			<span><img src="/images/note.gif" alt="Tip" height="13" width="15" > Leave blank to disable</span>~;
			Custom::Toolbar::advToolbar("forum_rules", $FORM{easycodeblock}, $FORM{smilieblock}, $FORM{html}, "");
			print qq~
			</div>
		</td>
	</tr>
	</table>
	<!-- End General Options -->
	</div>
	</div>
	
	<script>document.write('<div class="box" style="display:none"><h1></h1>')</script>
	<noscript><div class="box" style="display:block"><h1></h1></noscript>
	<!-- Begin Security Options -->
	<table width="490" border="0" cellspacing="0" cellpadding="6" class="text">
	<noscript>
	<tr>
		<td colspan="2" class="heading">Security Settings:</td>
	</tr>
	</noscript>
	<tr> 
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)"> 
		<td nowrap><a name="app"></a><span onclick="toggleTooltip('Registration Approval','This feature will allow you to approve each user before they can begin using your forum as a normal user. When a new user registers an account in your forum, they would be put into the Pending Members user group. They would be moved into the Registered Users user group once they are approved by a moderator who has been granted permission to approve users. You can <a href=&quot;/tool/members/mb/usergroup&quot;>edit the user group permissions</a> of the Pending Members user group to restrict pending members.<p>Note: When you turn on registration approval your current members will not need to be approved, only new members.', this);" class="help_tooltip_img" title="Help"></span> Require approval of new registrations:</td>
		<td><input type="checkbox" name="reqregapp" value="checked" id="REQregapp" approvalMessage(this);" $FORM{reqregapp}><label for="REQregapp" title="Require registration approval" style="cursor:pointer"> Yes </label></td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)"> 
		<td nowrap><span onclick="toggleTooltip('Email Confirmation','How does the user confirm their email address?<br><br>An email is sent to the user immediately after they register, the user then has to click a link in the email that will confirm that their email address is valid.<hr noshade>Moderators can resend the confirmation email through the pending member\\'s profile.<p>Note: Accounts that have been pending email confirmation for more than one month will automatically be deleted.', this);" class="help_tooltip_img" title="Help"></span> Require users to confirm their email address:</td>
		<td><input type="checkbox" name="confirm_email" value="checked" id="confemail" $FORM{confirm_email}><label for="confemail" title="Confirm email address" style="cursor:pointer"> Yes </label></td>
	</tr>
		<tr onmouseover="mOvr(this)" onmouseout="mOut(this)"> 
		<td nowrap><span onclick="toggleTooltip('Multiple accounts per user','Enabling this option will allow your users to register for multiple accounts in your forum.<p>Disabling this feature is recommended so that each user has a unique identity.<p>The system stops multiple registrations per user by checking the email address entered by the user to determine if an account has already been created with the same email address.', this);" class="help_tooltip_img" title="Help"></span> Allow users to have multiple accounts:</td>
		<td><input type="checkbox" name="allowmultiregs" value="checked" id="AMRS" $FORM{allowmultiregs}><label for="AMRS" title="Allow multiple accounts" style="cursor:pointer"> Yes </label></td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
		<td nowrap><span onclick="toggleTooltip('Allow user-to-user emailing','Enabling this option will allow users to email other users using a built-in email form on your forum.<p>Note: The user\\'s email address will never be publicly revealed.', this);" class="help_tooltip_img" title="Help"></span> Allow users to email other users:</td>
		<td><input type="checkbox" name="allow_emails" value="checked" id="aEMS" $FORM{allow_emails}><label for="aEMS" title="Allow users to send emails" style="cursor:pointer"> Yes </label></td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
		<td><span onclick="toggleTooltip('','Disabling this option will prevent new users from registering for an account on your forum.', this);" class="help_tooltip_img" title="Help"></span> Allow new user registrations:</td><td><input type="checkbox" name="new_user_registration" value="checked" id="new_user_registration" $FORM{new_user_registration}><label for="new_user_registration" title="Allow new user registrations" style="cursor:pointer"> Yes </label></td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)"> 
		<td nowrap><span onclick="toggleTooltip('Password Protection','This feature is used to password protect your forum so only people with the correct password can enter.<p>Visitors without this password will not be able to access any area of your forum, including all forums.<p>Leave the checkbox unchecked or the password box blank if you would not like to use password protection.<p>Note: You can password protect a single forum in the <a href=&quot;/cgi/members/forum.cgi&quot;>Manage Forums</a> section.', this);" class="help_tooltip_img" title="Help"></span> Use password protection:</td>
		<td> 
		<span id="forum_pw_cbl" style="display: none;"><input type="checkbox" name="forum_pw_cb" value="1" id="forum_pw_cb"><label style="cursor:pointer" for="forum_pw_cb"> Yes </label></span>
		<input type="password" name="pass" id="forum_pw" value="$FORM{pass}" maxlength=16 size=16 title="Forum password" placeholder="Forum password">
		</td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)"> 
		<td nowrap><span onclick="toggleTooltip('Post Image Verification','Turning this feature on will display an image with a few characters on it to your visitors when they are posting a message, posting an event, or sending an email. Your visitors will be required to type the characters on the image into a textbox.<p>This feature is used to verify that a human is posting the message rather than an automatic spam robot.<p>Your forum has a built-in security feature that will automatically prompt users with an image verification if their post looks like spam. Therefore, it is recommended that you only turn on image verification if you are having problems with spam on your forum.', this);" class="help_tooltip_img" title="Help"></span> Require image verification for posts:</td>
		<td><input type="checkbox" name="use_captcha" value="checked" id="captcha" $FORM{use_captcha} onClick="if (this.checked) toggleTooltip('Note', 'Your forum has a built-in security feature that will automatically prompt users with an image verification if their post looks like spam. Therefore, it is recommended that you only turn on image verification if you are having problems with spam on your forum.', this);"><label for="captcha" title="Enable CAPTCHAs" style="cursor:pointer"> Yes </label></td>
	</tr>
	
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)"> 
		<td nowrap><span onclick="toggleTooltip('Registration Image Verification','Turning this feature on will display an image with a few characters on it to your visitors when they are register there self as a new user. New user will be required to type the characters on the image into a textbox.<p>This feature is used to verify that a human is registering rather than an automatic spam robot.<p>Your forum has a built-in security feature that will automatically prompt users with an image verification if their registration looks like spam. Therefore, it is recommended that you only turn on image verification if you are having problems with spam on your forum.', this);" class="help_tooltip_img" title="Help"></span> Require image verification for registrations:</td>
		
		<td><input type="checkbox" name="use_captcha_registration" value="checked" id="captcha_registration" $FORM{use_captcha_registration} onClick="if (this.checked) toggleTooltip('Note', 'Your forum has a built-in security feature that will automatically prompt users with an image verification if their registration looks like spam. Therefore, it is recommended that you only turn on image verification if you are having problems with spam on your forum.', this);"><label for="captcha_registration" title="Enable CAPTCHAs" style="cursor:pointer"> Yes </label></td>
	</tr>
	<tr onmouseover="mOvr(this); showTip('username_regexp_tip');" onmouseout="mOut(this); hideTip('username_regexp_tip');"> 
		<td nowrap><span onclick="toggleTooltip('Username Regular Expression','You may require the username to match a regular expression. For example, you can require the username to be in the format of an email address, prevent spaces in the username, prevent international characters, etc.<p>Do not start or end the expression with an escape character.<p>Leave this field blank to disable this option and allow users to choose any username.', this);" class="help_tooltip_img" title="Help"></span>&nbsp;Username regular expression: </td>
		<td nowrap>
		<input type="text" size="25" maxlength="200" value="$FORM{username_regexp}" name="username_regexp" id="uregex_tb"/>
		&nbsp;<span id="username_regexp_tip" style="display: none;"><a href="#" onClick="toggleTooltip('',document.getElementById('usernameRegexp'),document.getElementById('uregex_tb')); tooltip.clickable='1'; return false;"><span class="button" style="vertical-align: middle;">Examples</span></a></span>
		</td>
	</tr>
	<tr onmouseover="mOvr(this); showTip('flood_tip');" onmouseout="mOut(this); hideTip('flood_tip');"> 
		<td nowrap><span onclick="toggleTooltip('Post flood prevention','You may prevent your users from flooding your forum with garbage posts by activating this feature.<p>By enabling post flood prevention, you prevent users from making another post within a given time span of their last posting. In other words, if you set this option to 30 seconds, a user may not post again within 30 seconds of making their last post.<p>Moderators are exempt from post flood prevention.<p>Enter 0 to disable this function.', this);" class="help_tooltip_img" title="Help"></span> Minimum time between posts:</td>
		<td nowrap>
		<input type="text" name="flood" value="$FORM{flood}" size=4> Seconds
		&nbsp;&nbsp;&nbsp;<span id="flood_tip" style="display: none;"><img src="/images/note.gif" alt="Tip" height="13" width="15"> Tip: Enter 0 to disable</span>
		</td>
	</tr>
	<!-- End Security Options -->
	<!-- Begin Filter Options -->
	<tr><td colspan="2"><br></td></tr>
      <tr>
		<td colspan="2" class="heading">Filter Settings:</td>
	</tr>
	<tr onmouseover="mOvr(this); showTip('vulgarity_lvl_tip');" onmouseout="mOut(this); hideTip('vulgarity_lvl_tip');">
		<td><span onclick="toggleTooltip('Profanity Filter','<b>Full Filter:</b><br>This option will block all profanity even if it begins or ends with other characters.<p><b>Light Filter:</b><br>This option will only block profanity that begins and ends with a space.<br><hr>For example: The text <i>shit..</i> will be blocked by the full filter but it will not be blocked by the light filter because the word is followed by a period.<p>Some people may want to turn this feature to light because it may cause problems while trying to post some words. For example: <i>scrape</i> contains the word <i>crap</i>, so it would be blocked by the full filter.', this);" class="help_tooltip_img" title="Help"></span> Profanity filter level:</td>
		<td>
		<select name="vulgarity_lvl">
		<option value="full" $FILTER{full}>Full
		<option value="light" $FILTER{light}>Light
		<option value="off" $FILTER{off}>Off
		</select>
		&nbsp;<span id="vulgarity_lvl_tip" style="display: none;"><a href="/cgi/members/blocked.cgi?type=profanity" title="Specify which words are blocked by the filter" onClick="return confirmExit();"><span class="button" style="vertical-align: middle;">Edit Filter</span></a></span>
		</td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
		<td><span onclick="toggleTooltip('HTML Filter','Enabling this option will cause the system to automatically convert any HTML coding that a user posts to plain text.', this);" class="help_tooltip_img" title="Help"></span> Enable HTML filter:</td>
		<td><input type="checkbox" name="htmlblock" value="checked" id="htmlB" $FORM{htmlblock}><label for="htmlB" title="Block html" style="cursor:pointer"> Yes </label></td>
	</tr>
	<tr><td colspan=2><br></td></tr>
	 </table>
	<!-- End Filter Options -->
	</div>
	

	<script>document.write('<div class="box" style="display:none"><h1></h1>')</script>
	<noscript><div class="box" style="display:block"><h1></h1></noscript>
	<!-- Begin Notification Options -->
	<table width="490" border="0" cellspacing="0" cellpadding="6" class="text">
	<noscript>
	<tr>
		<td colspan="2" class="heading">Notification Settings:</td>
	</tr>
	</noscript>

	<tr onmouseover="mOvr(this);" onmouseout="mOut(this);">
		<td nowrap><span onclick="toggleTooltip('','Entering email addresses here will cause an email to be sent to each address when a new topic is posted on your forum. Separate each email address with a comma.', this);" class="help_tooltip_img" title="Help"></span> Email addresses to notify when a new topic is posted:</td>
		<td><textarea wrap="virtual" cols="20" rows="3" name="notify" style="width: 250px;" onFocus="showTip('comma_tip_1');" onBlur="hideTip('comma_tip_1');">$FORM{notify}</textarea><span id="comma_tip_1" style="display: none;"><br>(Separated by a comma)</span></td>
	</tr>
	<tr onmouseover="mOvr(this);" onmouseout="mOut(this);">
		<td nowrap><span onclick="toggleTooltip('','Entering email addresses here will cause an email to be sent to each address when a new reply is posted on your forum. Separate each email address with a comma.', this);" class="help_tooltip_img" title="Help"></span> Email addresses to notify when a new reply is posted:</td>
		<td><textarea wrap="virtual" cols="20" rows="3" name="notifyreply" style="width: 250px;" onFocus="showTip('comma_tip_2');" onBlur="hideTip('comma_tip_2');">$FORM{notifyreply}</textarea><span id="comma_tip_2" style="display: none;"><br>(Separated by a comma)</span></td>
	</tr>
	<tr onmouseover="mOvr(this);" onmouseout="mOut(this);"> 
		<td nowrap><span onclick="toggleTooltip('','Entering email addresses here will cause an email to be sent to each address when a new member is registered on your forum. Separate each email address with a comma.', this);" class="help_tooltip_img" title="Help"></span> Email addresses to notify when a new registration occurs:</td>
		<td><textarea wrap="virtual" cols="20" rows="3" name="notifyreg" style="width: 250px;" onFocus="showTip('comma_tip_3');" onBlur="hideTip('comma_tip_3');">$FORM{notifyreg}</textarea><span id="comma_tip_3" style="display: none;"><br>(Separated by a comma)</span></td>
	</tr>
	
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)"> 
		<td nowrap><span onclick="toggleTooltip('Allow topic subscriptions','Enabling this option will allow users to receive email notifications of new replies to a topic by subscribing to it.<p>Note: Every notification email will contain a link that can be used to unsubscribe from the topic. The user\\'s email address will never be publicly revealed or misused.', this);" class="help_tooltip_img" title="Help"></span> Allow users to subscribe to a topic:</td>
		<td><input type="checkbox" name="allow_subscribe" value="checked" id="aSBSRB" $FORM{allow_subscribe}><label for="aSBSRB" title="Allow topic subscriptions" style="cursor:pointer"> Yes </label></td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)"> 
		<td nowrap><span onclick="toggleTooltip('Allow forum subscriptions','Enabling this option will allow users to receive email notifications of new topics and replies in a forum by subscribing to it.<p>Note: Every notification email will contain a link that can be used to unsubscribe from the forum. The user\\'s email address will never be publicly revealed or misused.', this);" class="help_tooltip_img" title="Help"></span> Allow users to subscribe to a forum:</td>
        	<td><input type="checkbox" name="allow_forum_subscribe" value="checked" id="aFSBSRB" $FORM{allow_forum_subscribe} ><label for="aFSBSRB" title="Allow forum subscriptions" style="cursor:pointer"> Yes </label></td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)"> 
		<td nowrap><a name=reg></a><span onclick="toggleTooltip('','This is the email address that should be displayed in the <i>From</i> field for emails that are sent by the system to users of your forum during certain cases. For example, when the user registers a new account, receives a notification for a topic they have subscribed to, etc.', this);" class="help_tooltip_img" title="Help"></span> Email address for system emails:</td>
		<td><input type="text" name="system_email" value="$FORM{system_email}" id="REQsystem_email"></td>
	</tr>
	<!-- End Notification Options -->
	</table>
	</div>
	

	<script>document.write('<div class="box" style="display:none"><h1></h1>')</script>
	<noscript><div class="box" style="display:block"><h1></h1></noscript>
	<!-- Begin Time Options -->
	<table width="490" border="0" cellspacing="0" cellpadding="6" class="text">
	<noscript>
	<tr>
		<td colspan="2" class="heading">Date Settings:</td>
	</tr>
	</noscript>
  <tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
		<td><span onclick="toggleTooltip('','Specifies how the date will appear.', this);" class="help_tooltip_img" title="Help"></span> Date format:
		</td>
		<td>
		<select name="date_format" tabindex=10>
		<option value="1" $DATE_FORMAT{'1'}>mm/dd/yy</option>
		<option value="2" $DATE_FORMAT{'2'}>dd/mm/yy</option>
		<option value="3" $DATE_FORMAT{'3'}>month dd, year</option>
		</select>
		</td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)"> 
		<td nowrap><span onClick="toggleTooltip('','This is the time zone that will be used by default to calculate dates and times for guests and new user accounts. Users will be able to change their time zone from the default while registering a new account.', this);" class="help_tooltip_img" title="Help"></span> Default time zone:</td>
		<td nowrap><input type="text" name="timeoffset" value="$FORM{timeoffset}" size=4 maxlength=4> <span id="dialog" class="button" style="vertical-align: middle;">Choose</span></a></td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)"> 
		<td nowrap><span onclick="toggleTooltip('Daylight Saving Time (DST)','If this option is enabled, the system will automatically adjust the date and time if Daylight Saving Time is taking place in your time zone. In certain rare cases, you may want to turn this option off if you find that the system is incorrectly detecting the DST in your time zone.', this);" class="help_tooltip_img" title="Help"></span> Automatically adjust time for Daylight Saving Time:</td>
		<td><input type="checkbox" name="dst" value="checked" id="DST" $FORM{dst}><label for="DST" title="DST" style="cursor:pointer"> Yes </label></td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)"> 
		<td nowrap><span onClick="toggleTooltip('','Enabling this option will cause the time to be displayed next to most dates. For example, May 10, 2012 at 3:52 PM instead of just May 10, 2012.', this);" class="help_tooltip_img" title="Help"></span> Time format:</td>
		<td>
			<select name="display_time" tabindex=10>
				<option value="1" $TIME_FORMAT{'1'}>12-Hour Clock</option>
				<option value="2" $TIME_FORMAT{'2'}>24-Hour Clock</option>
				<option value="0" $TIME_FORMAT{'0'}>Hide the time</option>
			</select>
		</td>
	</tr>
	<tr><td colspan=2><br></td></tr>
	</table>
	<!-- End Time Options -->
	</div>
	

	<!-- Begin Chat Room Options -->
	<script>document.write('<div class="box" style="display:none"><h1></h1>')</script>
	<noscript><div class="box" style="display:block"><h1></h1></noscript>
	<table width="490" border="0" cellspacing="0" cellpadding="6" class="text">
	<noscript>
	<tr>
		<td colspan="2" class="heading">Chat Room Settings:</td>
	</tr>
	</noscript>
	
	<tr>
		<td class="heading" colspan="2">Chat Room Options:</td>
	</tr>
	
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
		<td><span onclick="toggleTooltip('Chat room link','Enabling this option will add a \\'Chat\\' link to your forum navigation that can be clicked to launch your chat room.', this);" class="help_tooltip_img" title="Help"></span> Display a chat room link in the navigation area:</td>
		<td><input type="checkbox" name="chat_link" value="checked" id="cRMLK" $FORM{chat_link} ><label for="cRMLK" title="Display chat room link" style="cursor:pointer"> Yes </label></td>
    </tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
		<td><span onclick="toggleTooltip('Active chat users list','Enable this option to display a list of online chat users on the main forum page.', this);" class="help_tooltip_img" title="Help"></span> Display list of active chat room users:</td>
		<td><input type="checkbox" name="active_chat_users" value="checked" id="aACTUSR" $FORM{active_chat_users} ><label for="aACTUSR" title="Display chat room link" style="cursor:pointer"> Yes </label></td>
    </tr>
	<tr><td colspan="2"><br></td></tr>
	<tr>
		<td class="heading" colspan="2">Chat Bar Options:</td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
		<td><span onclick="toggleTooltip('Enable the chat bar','Enabling this option will display a floating chat bar at the bottom of your forum pages. The chat bar allows you to have live discussions with other users who are browsing the forum without leaving the page.', this);" class="help_tooltip_img" title="Help"></span> Enable the chat bar:</td>
		<td><input type="checkbox" name="enable_chat_bar" value="checked" id="eChatbar" $FORM{enable_chat_bar}><label for="eChatbar" title="Enable the chat bar" style="cursor:pointer"> Yes </label></td>
    </tr>
	</table>
	</div>
	<!-- End Chat Room Options -->
	<script>document.write('<div class="box" style="display:none"><h1></h1>')</script>
	<noscript><div class="box" style="display:block"><h1></h1></noscript>
	<!-- Begin Single Signon Options -->
	<table width="490" border="0" cellspacing="0" cellpadding="6" class="text">
	<noscript>
	<tr> 
		<td colspan="2" class="heading">Enable single sign-on:</td>
	</tr>
	</noscript>
	<tr>
		<td colspan="2" align="justify">The SSO API allows you to integrate your forum's registration, login, and logout process with your website. <a href="http://www.websitetoolbox.com/tool/support/241">Setup Instructions...</a><br><br></td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
		<td nowrap><span onclick="toggleTooltip('API Key','The API Key is passed as a parameter in your API calls to verify that you are an authorized user of the API. Your API Key is like a password to your account and should be kept private and secure.', this);" class="help_tooltip_img" title="Help"></span> API Key:</td>
		<td><input type="text" name="apikey" id="apikeyid" value="$FORM{apikey}" size="15" readonly="true" onclick="this.focus(); this.select();"> <a onclick="return generateApiKey();" href="/cgi/members/mboard.cgi?action=generateapikey"><span class="button">Regenerate</span></a></td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
		<td nowrap><span onclick="toggleTooltip('Login URL','Use this option if you have setup Single Sign On using our API. If a login page URL is provided, clicking on the \\'Login\\' link in your forum will automatically take the user to your website\\'s login page.', this);" class="help_tooltip_img" title="Help"></span> Login page:</td>
		<td><input type="text" name="login_page_url" value="$FORM{login_page_url}" size="40"></td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
		<td nowrap><span onclick="toggleTooltip('Logout page URL','Use this option if you have setup Single Sign On using our API. If a logout page URL is provided, clicking on the \\'Logout\\' link in your forum will automatically take the user to your website\\'s logout page. It will redirect to your website\\'s logout page after getting logged out from the forum.', this);" class="help_tooltip_img" title="Help"></span> Logout page:</td>
		<td><input type="text" name="logout_page_url" value="$FORM{logout_page_url}" size="40"></td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
		<td nowrap><span onclick="toggleTooltip('Registration URL','Use this option if you have setup Single Sign On using our API. If a registration page URL is provided, clicking on the \\'Register\\' link in your forum will automatically take the user to your website\\'s register page.', this);" class="help_tooltip_img" title="Help"></span> Registration page:</td>
		<td><input type="text" name="registration_url" value="$FORM{registration_url}" size="40"></td>
	</tr>
	~;
	
	my $saml_enabled = 0;
	if ($saml_enabled) {
		print qq~
		<tr> 
			<td colspan="2"></td>
		</tr>
		<tr> 
			<td colspan="2" class="heading">SAML:</td>
		</tr>
		<tr>
			<td colspan="2" align="justify">SAML is an XML standard that allows secure web domains to exchange user authentication and authorization data. Using SAML, Website Toolbox can communicate with your system to authenticate users who are trying to access your forum through an idP. This will allow your forum login and registration process to seamlessly integrate with your existing login and registration process.<br>
			</td>
		</tr>
		<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
			<td nowrap><span onclick="toggleTooltip('Enable SAML integration','SAML integration allows your website users to login once in your website and automatically gain access in the forum without being prompted to login again. It also provides you the facility of Single Sign Off, whereby the users of your website will automatically be logged out from forum if they sign out from your website. You must setup an idP on your server to use SAML authentication.', this);" class="help_tooltip_img" title="Help"></span> Enable SAML integration:</td>
			<td><input type="checkbox" name="sso_enabled" value="checked" id="SAML_ENABLED" onClick="enabledSaml();"  $FORM{sso_enabled}><label for="SAML_ENABLED" style="cursor:pointer" title="Enable SAML integration"> Yes </label></td>
		</tr>
		<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
			<td nowrap><span onclick="toggleTooltip('My idP is publicly available','If your idP is public and available on the internet, you may want to select this option so that WT service provider can contact your online idP to send the authentication request. In case your idP is not accessible over internet, you should not select this option because in this case you may only want to send the authentication response to WT service provider.', this);" class="help_tooltip_img" title="Help"></span> My idP is publicly available:</td><td><input type="checkbox" name="allow_two_way_sso" value="checked" id="allow_two_way_sso" onClick="TwoWayLoginLogout('1');" $FORM{allow_two_way_sso}><label for="allow_two_way_sso" title="My idP is publicly available" style="cursor:pointer"> Yes </label></td>
		</tr>
		<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
			<td nowrap><span onclick="toggleTooltip('Identity provider URL','The identity provider or idP is a kind of service of your website that creates, maintains, and manages identity information of your website users. Website Toolbox service provider will contact your online identity provider to authenticate your website users who are trying to access and use secure forum. Please provide here the location of your idP.', this);" class="help_tooltip_img" title="Help"></span> Identity provider URL:</td>
			<td><input type="text" name="idp_login_url" value="$FORM{idp_login_url}" size="40"></td>
		</tr>
		<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
			<td nowrap><span onclick="toggleTooltip('Logout request listener URL','This is the location of your idP logout request listener. Website Toolbox need this information to send the Single Sign-Off requests when users of forum sign out from the forum.', this);" class="help_tooltip_img" title="Help"></span> Logout request listener URL:</td>
			<td><input type="text" name="customer_logout_request_listener_url" value="$FORM{customer_logout_request_listener_url}" size="40"></td>
		</tr>
		<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
			<td nowrap><span onclick="toggleTooltip('Logout response listener URL','This is the location of your idP logout response listener. Website Toolbox need this information to send the Single Sign-Off response to inform your idP after a Sign Off request from your idP has completed by the forum.', this);" class="help_tooltip_img" title="Help"></span> Logout response listener URL:</td>
			<td><input type="text" name="customer_logout_response_listener_url" value="$FORM{customer_logout_response_listener_url}" size="40"></td>
		</tr>
		<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
			<td><span onclick="toggleTooltip('Use digital signature','For an added security, if you want to use SAML request or response to be verified with X.509 digital signatures, you should select this option.', this);" class="help_tooltip_img" title="Help"></span> Use digital signature:</td>
			<td><input type="checkbox" name="digital_signature" value="checked" id="digital_signature" onClick="upload_certificate();" $FORM{digital_signature}><label for="digital_signature" title="Use digital signature" style="cursor:pointer"> Yes </label></td>
		</tr>~;

		if(!$certificate_exist){
			print qq~<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
			<td><span onclick="toggleTooltip('Your verification certificate','This is where you upload your X.509 certificate containing the public key. The certificate file must contain the public key for Website Toolbox to verify single sign-on requests.', this);" class="help_tooltip_img" title="Help"></span> Your verification certificate:</td>
			<td><input type="file" name="certificate" size="30"></td>
			</tr>~;
		} else {
		print qq~<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
			<td><span onclick="toggleTooltip('Your verification certificate','This is where you upload your X.509 certificate containing the public key. The certificate file must contain the public key for Website Toolbox to verify single sign-on requests.', this);" class="help_tooltip_img" title="Help"></span> Your verification certificate:</td><td><a href="/cgi/members/mboard.cgi?action=deletecertificate" onClick="return confirm('Are you sure you want to delete your certificate.');">Delete your certificate<a></td>
			</tr>~;
		}
		if(!$metadata_exist){
			print qq~<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
			<td><span onclick="toggleTooltip('Your meta data','This is where you have to publish the data about your identity provider. Your metadata will tell us each and everything about your idP. You have to upload a well formed xml document of your idP metadata here.', this);" class="help_tooltip_img" title="Help"></span> Your meta data:</td><td><input type="file" name="usermetadata" size="30"></td>
			</tr>~;
		} else {
			print qq~<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
			<td nowrap><span onclick="toggleTooltip('Your meta data','This is where you have to publish the data about your identity provider. Your metadata will tell us each and everything about your idP. You have to upload a well formed xml document of your idP metadata here.', this);" class="help_tooltip_img" title="Help"></span> Your meta data:</td>
			 <td nowrap><a href="/cgi/members/mboard.cgi?action=deletemetadata" onClick="return confirm('Are you sure you want to delete your metadata.');">Delete your metadata<a></td>
			</tr>~;
		}
		print qq~<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
			<td nowrap><span onclick="toggleTooltip('WT verification certificate','This is X.509 certificate containing the public key of Website Toolbox service provider.', this);" class="help_tooltip_img" title="Help"></span> WT verification certificate:</td><td><a href="/cgi/members/mboard.cgi?action=download">Download</a></td>
			</tr>
			<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
				<td nowrap><span onclick="toggleTooltip('WT metadata','Website Toolbox provides all information about its service provider in its metadata file. It is a well formed xml document that will let you know about our assertion consumer service location, the attributes we require, what binding schemes can be used with us and other useful information.', this);" class="help_tooltip_img" title="Help"></span> WT meta data:</td><td><a href="/cgi/members/mboard.cgi?action=downloadmetadata">Download</a></td>
			</tr>
			<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
				<td colspan="2"><span onclick="toggleTooltip('WT logout request listener','This is the location where your idP will send the logout request to Website Toolbox. This is needed when a user logs out from your website so that they can be logged out from Forum also.', this);" class="help_tooltip_img" title="Help"></span> WT logout request listener:</td>
			</tr>
			<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
				<td colspan="2">http://saml.websitetoolbox.com:8180/sp/logoutRequestHandler</td>
			</tr>
			<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
				<td colspan="2"><span onclick="toggleTooltip('WT logout response listener ','This is the location where your idP will send the logout response to Website Toolbox. This is needed when a user logs out from Forum and after logging out this user from your idP, you send a logout success or fail response Website Toolbox Service Provider.', this);" class="help_tooltip_img" title="Help"></span> WT logout response listener:</td>
			</tr>
			<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
				<td colspan="2">http://saml.websitetoolbox.com:8180/sp/logoutResponseHandler</td>
			</tr>
		~;
	}
	
	print qq~
		</table>
	</div>
	<!--  Single sign-on Options End-->
	
	<script>document.write('<div class="box" style="display:none"><h1></h1>')</script>
	<noscript><div class="box" style="display:block"><h1></h1></noscript>
	<!-- Begin File Uploading Settings Options -->
	<table width="490" border="0" cellspacing="0" cellpadding="6" class="text">
	<noscript>
	<tr> 
		<td colspan="2" class="heading">File Uploading Settings:</td>
	</tr>
	</noscript>
	
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
		<td nowrap><span onclick="toggleTooltip('Enable file attachments','Enabling this feature will allow your forum users to upload files and attach them to their posts.', this);" class="help_tooltip_img" title="Help"></span> File attachments:</td>
		<td><input type="checkbox" name="file_uploading" value="checked" id="FU" onClick="checkAttachments();" $FORM{file_uploading}><label for="FU" title="file attachments" style="cursor:hand"> Enable </label></td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
		<td nowrap><span onclick="toggleTooltip('Enable avatar uploading','Enabling this feature will allow your forum users to upload their own avatar.<p>Avatars are small images displayed under usernames in thread display and user info pages.', this);" class="help_tooltip_img" title="Help"></span> Avatar uploading:</td>
		<td><input type="checkbox" name="avatar_uploading" value="checked" id="AU" $FORM{avatar_uploading} $reg_disable><label for="AU" title="avatar uploading" style="cursor:hand"> Enable </label></td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
			<td><span onclick="toggleTooltip('','If you enable this option, users will be able to use profile pictures, which are small images (usually larger than avatars) that users can upload to their profile pages. You can set this per-usergroup with the Can Upload Profile Pictures setting in Usergroup Manager.', this);" class="help_tooltip_img" title="Help"></span> Profile pictures:</td>
			<td><input type="checkbox" name="profile_picture" value="checked" id="ppEnable" $FORM{profile_picture}><label for="ppEnable" style="cursor:pointer"> Enable </label></td>
		</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
		<td nowrap><span onclick="toggleTooltip('Maximum file size','Specify the maximum size in kilobytes (KB) that an upload may be.<p>1 KB = 1024 bytes, 1 MB = 1024 KB', this);" class="help_tooltip_img" title="Help"></span> Maximum file size:</td>
			<td nowrap><div id="maxfile_options"><input type="textbox" name="max_file_size" value="$FORM{max_file_size}" id="max_file_size" size=7 maxlength=7> KB</div> <div id="slider" class="ui-slider ui-slider-horizontal ui-widget ui-widget-content ui-corner-all"><a href="#" class="ui-slider-handle ui-state-default ui-corner-all"></a></div>&nbsp;&nbsp; <span id="slider_values">$max_file_size_human</span></td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
		<td nowrap><span onclick="toggleTooltip('Accepted file types','Specify the file types that are allowed to be uploaded.', this);" class="help_tooltip_img" title="Help"></span> Accepted file types:<p><img src="/images/arrow_small.gif" width=6 height=6> <a href="#"onClick="toggleTooltip('Common File Types',document.getElementById('tooltipFileTypes'),this); return false;" title="Choose from a list of file types">Browse file types</a></td>
		<td><textarea rows=5 cols=25 name=file_types onFocus="document.getElementById('tipComma').style.display='';" onBlur="document.getElementById('tipComma').style.display='none';">$FORM{file_types}</textarea>
			<span id="tipComma" style="display: none;"><br>(Separate by a space)</span>
			</td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
		<td nowrap>Send me a warning email when my...</td>
		<td>
			<select name="notification_preference">
				<option value=0 $SELECTED{0}>Bandwidth or storage space is low</option>
				<option value=1 $SELECTED{1}>Bandwidth is low</option>
				<option value=2 $SELECTED{2}>Storage space is low</option>
				<option value=3 $SELECTED{3}>Never warn me</option>
			</select>
		</td>
	</tr>
	<tr onmouseover="mOvr(this)" onmouseout="mOut(this)">
		<td nowrap><span onclick="toggleTooltip('Attachment Display','<b>Note:</b> Choosing thumbnails or links is useful in conserving bandwidth and in preventing large (dimensions) attached images from stretching the forum layout.<p><b>Thumbnails</b><p>A thumbnail is a smaller version of an image. When thumbnails are enabled attached images will be represented by a smaller version of that image. A user can then click on the thumbnail to view the full-size image.<p><b>Full-size images</b><p>Enabling this option will cause attached images to be displayed within the post in their full size.<p><b>Links</b><p>Enabling this option will cause attached images to be represented by a link within the post. A user can then click on the link to view the full-size image.', this);" class="help_tooltip_img" title="Help"></span> 
		Show attached images as:</td>
		<td>
			<select name="attachment_display">
				<option value="thumbnails" $SELECTED{thumbnails}>Thumbnails</option>
				<option value="full" $SELECTED{full}>Full-size images</option>
				<option value="links" $SELECTED{links}>Links</option>
			</select>
		</td>
	</tr>
		</table>
		</div>
	</div>
<table width="490" border="0" cellspacing="0" cellpadding="6" class="text">
<tr>
	<td colspan="2">
	<div align="center"><br>
	<input type="hidden" name="already" value="true">
	<input type="hidden" name="action" value="updatemb">
	<input type="hidden" name="uses_forums" value="$FORM{uses_forums}">
	<input type="hidden" name="uploaded_certificate" value="$certificate_exist">
	<input type="hidden" name="logo" value="$FORM{logo}">
	<input type="hidden" name="uploaded_metadata" value="$metadata_exist">
	<button class="button btn-m btn-blue" type="submit">Save</button>
	</div>
	</td>
</tr>
</table>
</form>
<div id="tooltipFileTypes" class="tooltip" style="display: none;">
	<div id="fileTypeMsg" style="display: none;"></div>
	<table cellpadding="4" class="text">
		<tr valign="top">
			<td>
				<span class=heading>Multimedia</span>
				<ul class="spacedList arrowList" style="padding-left: 20px;">
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">ASF</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">AVI</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">MID</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">MIDI</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">MOV</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">MP3</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">MPA</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">MPEG</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">MPG</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">QT</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">RA</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">RAM</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">RM</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">WAV</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">WMA</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">WMV</a>
				</ul>
			</td>
			<td>
				<span class=heading>Documents</span>
				<ul class="spacedList arrowList" style="padding-left: 20px;">
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">DOC</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">DOCX</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">LOG</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">PDF</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">PHP</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">PPS</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">PPT</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">PPTX</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">RTF</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">TXT</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">XLS</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">XML</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">HTML</a>
				</ul>
			</td>
			<td>
				<span class=heading>Archives</span>
				<ul class="spacedList arrowList" style="padding-left: 20px;">
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">CAB</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">GZ</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">GZIP</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">JAR</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">RAR</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">TAR</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">ZIP</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">7Z</a>
				</ul>
			</td>
			<td>
				<span class=heading>Graphics</span>
				<ul class="spacedList arrowList" style="padding-left: 20px;">
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">BMP</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">GIF</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">JPE</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">JPEG</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">JPG</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">PNG</a>
					<li><a href="#" onClick="addFileType(this); return false;" title="Allow this file type">PSD</a>
				</ul>
			</td>
		</tr>
	</table>
</div>
<div style="display: none;" id="dbox">
	<form name="tz">
		<font face=arial size=2>
			<br>
			~;
			$TIMEZONE{"$FORM{timeoffset}"} = "selected";
			print qq~
			<select name="timeoffset" onChange="document.posts.timeoffset.value = document.tz.timeoffset.value; \$('#dbox').dialog('close');">
				<option value="-12" $TIMEZONE{"-12"}>(GMT -12:00 hours) Eniwetok, Kwajalein</option>
				<option value="-11" $TIMEZONE{"-11"}>(GMT -11:00 hours) Midway Island, Samoa</option>
				<option value="-10" $TIMEZONE{"-10"}>(GMT -10:00 hours) Hawaii</option>
				<option value="-9" $TIMEZONE{"-9"}>(GMT -9:00 hours) Alaska</option>
				<option value="-8" $TIMEZONE{"-8"}>(GMT -8:00 hours) Pacific Time (US & Canada)</option>	
				<option value="-7" $TIMEZONE{"-7"}>(GMT -7:00 hours) Mountain Time (US & Canada)</option>
				<option value="-6" $TIMEZONE{"-6"}>(GMT -6:00 hours) Central Time (US & Canada), Mexico City</option>
				<option value="-5" $TIMEZONE{"-5"}>(GMT -5:00 hours) Eastern Time (US & Canada), Bogota, Lima, Quito</option>
				<option value="-4" $TIMEZONE{"-4"}>(GMT -4:00 hours) Atlantic Time (Canada), Caracas, La Paz</option>	
				<option value="-3.5" $TIMEZONE{"-3.5"}>(GMT -3:30 hours) Newfoundland</option>
				<option value="-3" $TIMEZONE{"-3"}>(GMT -3:00 hours) Brazil, Buenos Aires, Georgetown</option>
				<option value="-2" $TIMEZONE{"-2"}>(GMT -2:00 hours) Mid-Atlantic</option>
				<option value="-1" $TIMEZONE{"-1"}>(GMT -1:00 hours) Azores, Cape Verde Islands</option>
				<option value="0" $TIMEZONE{"0"}>(GMT) Western Europe Time, London, Lisbon, Casablanca, Monrovia</option>
				<option value="+1" $TIMEZONE{"+1"}>(GMT +1:00 hours) CET(Central Europe Time), Brussels, Copenhagen, Madrid, Paris</option>
				<option value="+2" $TIMEZONE{"+2"}>(GMT +2:00 hours) EET(Eastern Europe Time), Kaliningrad, South Africa</option>	
				<option value="+3" $TIMEZONE{"+3"}>(GMT +3:00 hours) Baghdad, Kuwait, Riyadh, Moscow, St. Petersburg, Volgograd, Nairobi</option>
				<option value="+3.5" $TIMEZONE{"+3.5"}>(GMT +3:30 hours) Tehran</option>
				<option value="+4" $TIMEZONE{"+4"}>(GMT +4:00 hours) Abu Dhabi, Muscat, Baku, Tbilisi</option>
				<option value="+4.5" $TIMEZONE{"+4.5"}>(GMT +4:30 hours) Kabul</option>
				<option value="+5" $TIMEZONE{"+5"}>(GMT +5:00 hours) Ekaterinburg, Islamabad, Karachi, Tashkent</option>
				<option value="+5.5" $TIMEZONE{"+5.5"}>(GMT +5:30 hours) Bombay, Calcutta, Madras, New Delhi</option>
				<option value="+6" $TIMEZONE{"+6"}>(GMT +6:00 hours) Almaty, Dhaka, Colombo</option>
				<option value="+7" $TIMEZONE{"+7"}>(GMT +7:00 hours) Bangkok, Hanoi, Jakarta</option>
				<option value="+8" $TIMEZONE{"+8"}>(GMT +8:00 hours) Beijing, Perth, Singapore, Hong Kong, Chongqing, Urumqi, Taipei</option>
				<option value="+9" $TIMEZONE{"+9"}>(GMT +9:00 hours) Tokyo, Seoul, Osaka, Sapporo, Yakutsk</option>
				<option value="+9.5" $TIMEZONE{"+9.5"}>(GMT +9:30 hours) Adelaide, Darwin</option>
				<option value="+10" $TIMEZONE{"+10"}>(GMT +10:00 hours) EAST(East Australian Standard), Guam, Papua New Guinea, Vladivostok</option>
				<option value="+11" $TIMEZONE{"+11"}>(GMT +11:00 hours) Magadan, Solomon Islands, New Caledonia</option>
				<option value="+12" $TIMEZONE{"+12"}>(GMT +12:00 hours) Auckland, Wellington, Fiji, Kamchatka, Marshall Island</option>
			</select>
		</font>
	</form>
</div>
<div id="vsmilies" style="display: none;">
	<input type="hidden" name="username" id="username" value="$FORM{username}">
</div>
<br>
<style>
#usernameRegexp a {
	display: block;
	text-decoration: none;
	padding: 7px;
	color: #000;
	background-color: #FFFFFF;
}
#usernameRegexp a:hover {
	background-color: #3366CC;
	color: #FFF;
}
</style>
<div id="usernameRegexp" class="tooltip" style="display: none; background-color: #FFF;">
	<a href="#" onclick="return fillRegExp('^[a-zA-Z_0-9 ]+\$');">^[a-zA-Z_0-9 ]+\$ - Alphanumeric characters including underscores and spaces.</a>

	<a href="#" onclick="return fillRegExp('^[a-zA-Z_0-9]+\$');">^[a-zA-Z_0-9]+\$ - Alphanumeric characters including underscores.</a>
	
	<a href="#" onclick="return fillRegExp('^(\\\\\\\w|\\\\-|\\\\_|\\\\\\\.)+\\\\\\\@((\\\\w|\\\\-|\\\\_)+\\\\.)+[a-zA-Z]{2,}\$');">^(\\w|\\-|\\_|\\.)+\\@((\\w|\\-|\\_)+\\.)+[a-zA-Z]{2,}\$ - Email addresses only.</a>

	<a href="#" onclick="return fillRegExp('^[a-zA-Z0-9 ]+\$');">^[a-zA-Z0-9 ]+\$ - Alphanumeric characters including spaces.</a>
	
	<a href="#" onclick="return fillRegExp('^[a-zA-Z_]+\$');">^[a-zA-Z_]+\$ - Combination of lower and upper case letters including underscores.</a>

	<a href="#" onclick="return fillRegExp('^[a-zA-Z ]+\$');">^[a-zA-Z ]+\$ - Combination of lower and upper case letters including spaces.</a>
	
	<a href="#" onclick="return fillRegExp('^[a-z ]+\$');">^[a-z ]+\$ - Lowercase letters from a-z including spaces.</a>

	<a href="#" onclick="return fillRegExp('^[A-Z ]+\$');">^[A-Z ]+\$ - Uppercase letters from A-Z including spaces.</a>

	<a href="#" onclick="return fillRegExp('^[a-zA-Z0-9]+\$');">^[a-zA-Z0-9]+\$ - Alphanumeric characters only.</a>
	
	<a href="#" onclick="return fillRegExp('^[a-zA-Z]+\$');">^[a-zA-Z]+\$ - Combination of lower and upper case letters.</a>

	<a href="#" onclick="return fillRegExp('^[a-z]+\$');">^[a-z]+\$ - Lowercase letters from a-z only.</a>

	<a href="#" onclick="return fillRegExp('^[A-Z]+\$');">^[A-Z]+\$ - Uppercase letters from A-Z only. </a>
</div>
<script language="JavaScript" src="/js/url.js"></script>
<script language="JavaScript" src="/js/window.js"></script>
<script language="JavaScript" src="/js/tooltip.js"></script>
<script language="JavaScript" src="/js/disable_option.js"></script>

<script language=javascript type="text/javascript">

// must be after the form fully loads
frm = document.posts;
~;

my $cr_settings = $DB{mb}->selectrow_hashref("SELECT uid,chat_room_user_limit FROM cr.settings WHERE uid='$uid'");

# disable the chat room options if no chat room settings defined yet
if ($cr_settings->{uid} == 0) {
	print qq~
	disableRow(frm.chat_link, true, crTooltipTxt);
	disableRow(frm.active_chat_users, true, crTooltipTxt);
	~;
	
# disable the chat room options if the product is disabled due to not being included in this plan
} elsif ($cr_settings->{chat_room_user_limit} == 0) {
	print qq~
	disableRow(frm.chat_link, true, upgradePlanTooltipTxt);
	disableRow(frm.active_chat_users, true, upgradePlanTooltipTxt);
	~;
}

my $cb_settings = $DB{mb}->selectrow_hashref("SELECT disabled FROM ajax_cr.settings WHERE uid='$uid'");

if ($cb_settings->{disabled} == 1) {
	print qq~
	disableRow(frm.enable_chat_bar, true, upgradePlanTooltipTxt);
	~;
}

print qq~
enableCal();
regcheck();
TwoWayLoginLogout();
enabledSaml();
upload_certificate();
easycodeCheck();
rssFeed();
//Initialize first tab to be displayed
show_next_tab('tab'+$tab_id, $tab_id-1, 0); 

</script>

~;
&toolsbottom;
exit;
} 
#########################################################
sub updatemb{
	&ctest("header");

	if ($FORM{pass} =~ /[^a-z0-9]/) {
		&showmbsettings("Your password cannot contain any symbols, capital letters, or spaces.");
	}

	if ($FORM{perpage} =~ /\D/ || !$FORM{perpage} || $FORM{perpage} > 100) {
		&showmbsettings("Error: You entered an invalid number of topics to display per page.<br>Please enter a number between 0 and 100.");
	}

	if ($FORM{replies} =~ /\D/ || !$FORM{replies} || $FORM{replies} > 50) {
		&showmbsettings("Error: You entered an invalid number of replies to display per page.<br>Please enter a number between 0 and 50.");
	}

	$FORM{timeoffset} = 0 if ($FORM{timeoffset} eq "-0" || $FORM{timeoffset} eq "+0");

	if ($FORM{timeoffset} =~ /[^0-9\.\-\+]/ || !Custom::Date::isValidOffset($FORM{timeoffset})) {
		&showmbsettings("Error: Invalid Time Zone - Please use the 'Choose' button to select your correct time zone.");
	}

	$FORM{siteurl} = "http://$FORM{siteurl}" if ($FORM{siteurl} && $FORM{siteurl} !~ /^https?:\/\//i);


	if ($FORM{system_email} !~ /^[-!#$%&\'*+\\.\/0-9=?A-Z^_`{|}~]+@([-0-9A-Z]+\.)+([0-9A-Z]){2,4}$/i) {
				&showmbsettings("Error: You entered an invalid email address");
		}

	$FORM{mod_display} = "$FORM{mod_display}$FORM{mod_display2}$FORM{mod_display3}";
	$FORM{display_icons} = "$FORM{display_icons3}$FORM{display_icons4}";
	
	# Validate length of username regular expression option
	if ($FORM{username_regexp} && length($FORM{username_regexp}) > 200) {
		&showmbsettings("Error: The length of the regular expression should not exceed more than 200 characters for the username regular expression option.");
	}


	###############
	# For notify topic emails 
	if ($FORM{notify}) {
		my ( $invalid_email_ids , $valid_email_ids ) = &validate_notify_email($FORM{notify});
		if (length($FORM{notify}) > 500) {
			&showmbsettings("Error: The length of email addresses should not exceeds more than 500 characters for the new topic notification option.");
		}
		if ($invalid_email_ids) {
			&showmbsettings("Error: The Following email addresses provided for the new topic notification option are invalid: $invalid_email_ids");
		}
		else {
		  $FORM{notify} = $valid_email_ids;
		}
		
	}
	###############
	# For notify reply emails 
	if ($FORM{notifyreply}) {
		my ( $invalid_email_ids , $valid_email_ids ) = &validate_notify_email($FORM{notifyreply});
		if (length($FORM{notifyreply}) > 500) {
			&showmbsettings("Error: The length of email addresses should not exceeds more than 500 characters for the new reply notification option.");
		}
		if ($invalid_email_ids) {
			&showmbsettings("Error: The Following email addresses provided for the new reply notification option are invalid: $invalid_email_ids");
		}
		else {
		  $FORM{notifyreply} = $valid_email_ids;
		}
	}
	###############
	# For new member registration emails 
	if ($FORM{notifyreg}) {
		my ( $invalid_email_ids , $valid_email_ids ) = &validate_notify_email($FORM{notifyreg});
		if (length($FORM{notifyreg}) > 500) {
			&showmbsettings("Error: The length of email addresses should not exceeds more than 500 characters for the new member registration notification option.");
		}
		if ($invalid_email_ids) {
			&showmbsettings("Error: The Following email addresses provided for the new member registration notification option are invalid: $invalid_email_ids");
		}
		else {
		  $FORM{notifyreg} = $valid_email_ids;
		}
	}
	###############
	$FORM{av_width} = uc($FORM{av_width});
	$FORM{av_height} = uc($FORM{av_height});
	$FORM{av_width} = "NA" if (!$FORM{av_width} || $FORM{av_width} =~ /[^0-9]/);
	$FORM{av_height} = "NA" if (!$FORM{av_height} || $FORM{av_height} =~ /[^0-9]/);

	$FORM{flood} = int $FORM{flood};

	# set options disabled because of no registration to on so that when
	# registration is activated again the options default to on
	# this won't matter in the scripts because reqreg is always checked too
	if (!$FORM{reqreg}) {
		$FORM{confirm_email} = "checked";
		$FORM{show_num_users} = "checked";
		$FORM{online_user_list} = "checked";
		$FORM{online_user_statistic} = "checked";
		$FORM{allow_pm} = "checked";
		$FORM{av_width} = "48"; 
		$FORM{av_height} = "48";
		$FORM{allow_forum_subscribe} = "checked";
	}

	$FORM{upcoming_events} = "5" if(!$FORM{enable_calendar});

	my ($acc_found,$orig_reqregapp,$org_confirmemail,$orig_forumsubscription,$orig_threadsubscription) = 
	$DB{mb} -> selectrow_array("SELECT uid,reqregapp,confirmemail,allow_forumsubscribe,allow_subscribe FROM settings WHERE uid='$uid'");

	# disable the chat room options if no chat room settings defined yet
	my $cr_uid = $DB{mb}->selectrow_array("SELECT uid FROM cr.settings WHERE uid='$uid'");
	if ($cr_uid == 0) {
		$FORM{chat_link} = "";
		$FORM{active_chat_users} = "";
	}

	$FORM{idp_login_url} = "http://$FORM{idp_login_url}" if ($FORM{idp_login_url} && $FORM{idp_login_url} !~ /^https?:\/\//i);
	$FORM{customer_logout_request_listener_url} = "http://$FORM{customer_logout_request_listener_url}" if ($FORM{customer_logout_request_listener_url} && $FORM{customer_logout_request_listener_url} !~ /^https?:\/\//i);	
	$FORM{customer_logout_response_listener_url} = "http://$FORM{customer_logout_response_listener_url}" if ($FORM{customer_logout_response_listener_url} && $FORM{customer_logout_response_listener_url} !~ /^https?:\/\//i);
	$FORM{logout_page_url} = "http://$FORM{logout_page_url}" if ($FORM{logout_page_url} && $FORM{logout_page_url} !~ /^https?:\/\//i);
	$FORM{registration_url} = "http://$FORM{registration_url}" if ($FORM{registration_url} && $FORM{registration_url} !~ /^https?:\/\//i);
	$FORM{login_page_url} = "http://$FORM{login_page_url}" if ($FORM{login_page_url} && $FORM{login_page_url} !~ /^https?:\/\//i);

	if($FORM{allow_two_way_sso}) {
		if(!$FORM{idp_login_url} || !$FORM{customer_logout_request_listener_url} || !$FORM{customer_logout_response_listener_url}) {
			&showmbsettings("Error: First three are mandatory URL for publicly available idP.");
		}
		if(!$FORM{logout_page_url}) {
			&showmbsettings("Error: The logout page URL is required if you are using a publicly available idP.");
		}
	}	

	# If SAML integration and digital signature is enabled then verification certificate is manadatory.
	if($FORM{sso_enabled} && $FORM{digital_signature} && !$FORM{uploaded_certificate}) {
		if(!$certificate_filepath)  {
			&showmbsettings("Error: You must upload your certificate file for SAML.");
		}
	}
	
	# WE are uploading the certificate of the user 
	if($FORM{sso_enabled} && $FORM{digital_signature}){	
		$filename = $certificate_filepath;
		$filename =~ s/^.*(\\|\/)//;
		#For IE
		$filename =~ s/ +/\_/g;
		#For Opera
		$filename =~ s/\"//g;
		my @filename=split(/\./, $filename);
		if($filename) {
			while (read($certificate_filepath, $buffer, 1024)) {
			$file .= $buffer;
			}
			if($file) {
				open(FILE,">/usr/local/etc/chat_bar/certs/$FORM{username}.$filename[1]");	
				print FILE $file;
				close(FILE);
			}
		}
	}

	# If SAML integration is enable then meta data is manadatory
	if($FORM{sso_enabled} && !$FORM{uploaded_metadata} && !$metadata_filepath){
		&showmbsettings("Error: You must upload your idP metadata file to use SAML authentication.");
	}

	# we are uploading metadata of user.
	if($FORM{sso_enabled}) {
		$metadata_filename = $metadata_filepath;
        $metadata_filename =~ s/^.*(\\|\/)//;
		#For IE
		$metadata_filename =~ s/ +/\_/g;
		#For Opera
		$metadata_filename =~ s/\"//g;
		my @metadata_filename=split(/\./, $metadata_filename);
		if($metadata_filename[1] ne "xml" &&  !$FORM{uploaded_metadata}){
			&showmbsettings("Error: Your Metadata contain valid xml file.");
		}
		if($metadata_filename) {
			while (read($metadata_filepath, $buffer1, 1024)) {
				$metadata_filename .= $buffer1;
			}
			if($metadata_filename) {
				open(FILE,">/usr/local/etc/chat_bar/metadata/$FORM{username}.$metadata_filename[1]");	
				print FILE $metadata_filename;
				close(FILE);
			}
		}
	}

	# if SAML integration is off then delete certificate and metadata.
	if(!$FORM{sso_enabled}) {
		$FORM{digital_signature}='';
		&deleteFile('meta');
		&deleteFile('cert');
	}

	# update existing record
	# make adjustments put them in proper usergroups, if turned off email confirmation
	if ($orig_confirmemail eq "checked" && $FORM{confirm_email} eq "") {
		$DB{mb} -> do("UPDATE members SET usergroupid='".( $orig_confirmemail || $FORM{reqregapp} ? Custom::MB::Usergroup::getDefaultUserGroupId('Pending Members') : Custom::MB::Usergroup::getDefaultUserGroupId('Registered Users'))."' WHERE uid='$uid' AND usergroupid='".Custom::MB::Usergroup::getDefaultUserGroupId('Users Awaiting Email Confirmation')."'");
	}

	# make adjustments if turned off registration approval
	if ($orig_reqregapp eq "checked" && $FORM{reqregapp} eq "") {
		my $pending_members = $DB{mb} -> do("UPDATE members SET usergroupid='".Custom::MB::Usergroup::getDefaultUserGroupId('Registered Users')."' WHERE uid='$uid' AND usergroupid='".Custom::MB::Usergroup::getDefaultUserGroupId('Pending Members')."'");
		$DB{mb} -> do("UPDATE stats SET members=members+$pending_members WHERE uid='$uid'") if $pending_members
	}
	
	# delete forum subscriptions if turned off forum subscription
	if ($orig_forumsubscription eq "checked" && $FORM{allow_forum_subscribe} eq "") {
		$DB{mb} -> do("DELETE FROM subscribeforum WHERE uid='$uid'");
	}

	# delete topic subscription if turned off topic subscription
	if ($orig_threadsubscription eq "checked" && $FORM{allow_subscribe} eq "") {
		$DB{mb} -> do("DELETE FROM subscribethread WHERE uid='$uid'");
	}
	
	# For File Uploading settings
	if (!$FORM{max_file_size} || $FORM{max_file_size} =~ /\D/ || $FORM{max_file_size} > 51200) {
		&showmbsettings("Error: You entered an invalid maximum file size.");
	}

	$FORM{file_types} =~ s/\r\n|\r|\n|,|  / /g;

	if ($FORM{file_types} =~ /[^A-Za-z0-9 ]/) {
		&showmbsettings("Error: The accepted file types cannot contain any symbols.");
	}

	if (length $FORM{file_types} > 250) {
		$length = length $FORM{file_types};
		&showmbsettings("Error: The file types field is too long ($length characters). Please shorten it to 250 characters.");
	}

	$FORM{file_types} = lc($FORM{file_types});

	@types = split(/\s+/, $FORM{file_types});

	foreach (@types) {
		if ($_ eq "com" || $_ eq "vbs" || $_ eq "pif" || $_ eq "scr") {
			&showmbsettings("Error: $_ is not an acceptable file type.");
		}
	}
	my $forum_rule = $FORM{forum_rules};
	$forum_rule =~ s/<.+?>//g;
	$forum_rule =~ s/&nbsp;//g;
	if($forum_rule eq '') {
		$FORM{forum_rules} = '';
	}
	$DB{mb} -> do("UPDATE settings SET title='".&slash("$FORM{title}")."', threadsperpage='$FORM{perpage}', repliesperpage='$FORM{replies}', showlinkback='$FORM{slb}', displayicons='$FORM{display_icons}', protectionpw='".&slash("$FORM{pass}")."', flood='$FORM{flood}', profanitylvl='$FORM{vulgarity_lvl}', htmlfilter='$FORM{htmlblock}', notifythread='".&slash($FORM{notify})."',notifyreply='".&slash($FORM{notifyreply})."', enablesmilies='$FORM{smilie}', enableeasycode='$FORM{easycode}', timeoffset='$FORM{timeoffset}', dst='$FORM{dst}', displaytime='$FORM{display_time}', reqreg='$FORM{reqreg}', reqregapp='$FORM{reqregapp}', notifyreg='".&slash($FORM{notifyreg})."', confirmemail='$FORM{confirm_email}', shownumusers='$FORM{show_num_users}', allowpm='$FORM{allow_pm}', avatarwidth='$FORM{av_width}', 
	avatarheight='$FORM{av_height}', moddisplay='$FORM{mod_display}', spellcheck='$FORM{enable_spellcheck}', wysiwyg='$FORM{wysiwyg}', allow_emails='$FORM{allow_emails}', allow_subscribe='".&slash($FORM{allow_subscribe})."', allowmultiregs='$FORM{allowmultiregs}', use_captcha='$FORM{use_captcha}',use_captcha_registration='$FORM{use_captcha_registration}', sitename='".&slash($FORM{sitename})."', siteurl='".&slash($FORM{siteurl})."', dateformat='".&slash($FORM{date_format})."', threadreview='".&slash($FORM{allowthreadreview})."', allow_forumsubscribe='".&slash($FORM{allow_forum_subscribe})."', enable_rssfeed='".&slash($FORM{enable_rssfeed})."', rssfeed='".&slash($FORM{allow_rss_feed})."', chat_link='$FORM{chat_link}', active_chat_users='$FORM{active_chat_users}', enable_chat_bar='$FORM{enable_chat_bar}', 
	allow_views_column='$FORM{views_col}', enable_calendar='$FORM{enable_calendar}', system_email='".&slash($FORM{system_email})."', upcoming_events='$FORM{upcoming_events}', enable_polls='$FORM{enable_polls}', display_birthday='$FORM{display_birthday}', online_user_list = '$FORM{online_user_list}', online_user_statistic = '$FORM{online_user_statistic}', body_page_title = '$FORM{body_page_title}', new_user_registration = '$FORM{new_user_registration}', enable_social_bookmarking='$FORM{enable_social_bookmarking}',  word_wrap='$FORM{word_wrap}',quick_reply='$FORM{quick_reply}',idp_login_url='$FORM{idp_login_url}',customer_logout_request_listener_url='$FORM{customer_logout_request_listener_url}',customer_logout_response_listener_url='$FORM{customer_logout_response_listener_url}',logout_page_url='$FORM{logout_page_url}', 
	registration_url='$FORM{registration_url}', login_page_url='$FORM{login_page_url}',  username_regexp='".&slash($FORM{username_regexp})."',sso_enabled='$FORM{sso_enabled}',allow_two_way_sso='$FORM{allow_two_way_sso}',show_private_forums='$FORM{show_private_forums}',file_uploading='$FORM{file_uploading}',avatar_uploading='$FORM{avatar_uploading}',profile_picture='$FORM{profile_picture}',max_file_size='$FORM{max_file_size}',file_types='$FORM{file_types}',notification_preference='$FORM{notification_preference}',attachment_display='$FORM{attachment_display}',forum_rules='".&slash($FORM{forum_rules})."',enable_albums='$FORM{enable_albums}'WHERE uid = '$uid'");
		
    &showmbsettings("Your forum settings have been updated");
}
###########################################################################

#################################
#Purpose: This function is used to collect the invalid email address.
#Param1 – Comma separated email address.
#Returns- Invalid email address.
################################

sub validate_notify_email {
	my $notify_email_id = shift;
	my $invalid_email_id = undef;
	my $valid_email_id = undef;
	my @notify_emails = split(/,+/, $notify_email_id);
	if (@notify_emails) {
		foreach my $email(@notify_emails) {
			
			my $trim_email = &trim($email);
			if ($trim_email !~ /^[-!#$%&\'*+\\.\/0-9=?A-Z^_`{|}~]+@([-0-9A-Z]+\.)+([0-9A-Z]){2,4}$/i) {
				$invalid_email_id .= $trim_email."," ;
				next;
			}
			else {
				$valid_email_id .= $trim_email."," ;
				next;
			}
		}
		$invalid_email_id =~ s/,$//i;
		$valid_email_id =~ s/,$//i;
		return ($invalid_email_id , $valid_email_id);
	}
}

#################################
#Purpose: This function is used to trim spaces email address.
#Param1 –Email address to be trimmed .
#Returns-  email address with trimmed spaces.
################################

sub trim {
	my $string = shift;
	$string =~ s/^\s+//;
	$string =~ s/\s+$//;
	return $string;
}



###########################################################################
#puropse: This subroutine is used to delete the uploaded certificate of the user.
sub delte_doc {
	&deleteFile('cert');
	&showmbsettings("Your Certificate has been deleted.");	
	exit;	
}
#puropse: This subroutine is used to delete the specified file like certificate or metadata.
#param: file type (cert or meta)
sub deleteFile {
	my $file_type= shift;
	my $file_path;
	if($file_type eq 'cert') {
		# The Path of url where client's certificate is uploaded
		$file_path = "/usr/local/etc/chat_bar/certs/";
	} elsif ($file_type eq 'meta') {
		# The Path of url where client's metadata is uploaded
		$file_path = "/usr/local/etc/chat_bar/metadata/";
	}
	my (@files,$file);
	opendir(DIR, $file_path);
	@files = readdir(DIR);
	# we are opening the file location and checking wheather the file exist in the directory if the file name contain exact user name we are then deleting that file.
	my @matches = grep /^$FORM{username}\./, @files;
	foreach $file (@matches){
		unlink $file_path . '/' . $file;
	}
	close(DIR);
}

#puropse : This subroutine is used to delete the uploaded metadata of the user.
sub delte_metadata {
	&deleteFile('meta');
	&showmbsettings("Your Metadata has been deleted.");	
	exit;	
}

#puropse : This subroutine is used to download Websitet Toolbox certificate .
sub download_certificate {
	my $file = "wtb_certificate.cert";
	my $path_to_files="/usr/local/www/apache22/data/chat_bar/";
	open(my $DLFILE, '<', "$path_to_files/$file") or die "Can't open file '$path_to_files/$file' : $!";
	# This prints the download headers with the file size included
	print $req->header(-type => 'application/x-download',
		-attachment => $file,
		'Content-length' => -s "$path_to_files/$file",
	);
	binmode $DLFILE;
	print while <$DLFILE>;
	undef ($DLFILE);
	exit; 
}

#puropse : This subroutine is used to download Websitet Toolbox metadata.
sub download_metadata {
	my $file = "wtb_metadata.xml";
	my $path_to_files="/usr/local/etc/chat_bar/metadata/";
	open(my $DLFILE, '<', "$path_to_files/$file") or die "Can't open file '$path_to_files/$file' : $!";
	# This prints the download headers with the file size included
	print $req->header(-type => 'application/x-download',
		-attachment      => $file,
		'Content-length' => -s "$path_to_files/$file",
	);
	binmode $DLFILE;
	print while <$DLFILE>;
	undef ($DLFILE);
	exit;
}

#puropse : This subroutine is used to generate an API key which is used for API authintication.
sub generateApiKey {
	my @alphanumeric = ('a'..'z', 'A'..'Z', 0..9);
	my $ApiKey = join '', map $alphanumeric[rand @alphanumeric], 0..10;
	$DB{mb} -> do("UPDATE settings SET apikey='$ApiKey' WHERE uid='$uid'");
	if($FORM{ajax_request}) {
		print "Content-type: text/html\n\n";
		print $ApiKey;
	} else {
		&showmbsettings("API Key has been regenerated.");
	}
	exit;
}

#########################################################
sub type {

	my ($num) = @_;
	my ($type);

	$num = 0 if $num eq "";
	$type = "Bytes";

	if ($num >= 1024) {
		$num /= 1024;
		$type = "KB";
	}

	if ($num >= 1024) {
		$num /= 1024;
		$type = "MB";
	}

	if ($num >= 1024) {
		$num /= 1024;
		$type = "GB";
	}

	if ($num =~ /\./) {
		$num = sprintf("%.2f", $num);
	}

	return("$num $type");

}
