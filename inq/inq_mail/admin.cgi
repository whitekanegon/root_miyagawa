#!/usr/bin/perl

#======================================================================================
#	基本メールフォーム CGI　v1.0　Directed By PenguinNoise J.KANEDA
#
#   管理画面プログラム
#======================================================================================


# 外部ファイル取り込み
require './setting.cgi';
require $cgilib;

use lib $lib;
use Jcode;

&decode;
&times;
&open_kihon;

&passwd unless($passwd_form);
&passwd("<br><font color=#cc0000>パスワードが間違っています。</font>") unless($passwd_form eq $passwd);
if($regist) {&kanryo;}
elsif($mode eq 'kihon') {&kihon;}
elsif($mode eq 'mail_admin') {&mail_admin;}
elsif($mode eq 'mail_henshin') {&mail_henshin;}
else{&top;}

#------------------------------------------------------------------------------
# トップ表示
#------------------------------------------------------------------------------
sub top{
	
	open (IN,"$skin_top") || &error("$skin_topが開けません。");
	&header;
	while(<IN>){
		$_ =~ s/\$admin_script/$admin_script/g;
		s/!passwd!/$passwd_form/;
		
		# シフトJISコード変換
		Jcode::convert(\$_, 'utf8');
		
		print "$_";
	}
	close(IN);

}

#------------------------------------------------------------------------------
# 基本情報表示
#------------------------------------------------------------------------------
sub kihon{
	
	if($henshin_sign eq 'on'){
		$checked1 = ' checked';
		$checked2 = '';
	}else{
		$checked1 = '';
		$checked2 = ' checked';
	}
	
	open (IN,"$skin_kihon") || &error("$skin_kihonが開けません。");
	&header;
	while(<IN>){
		s/\$admin_script/$admin_script/g;
		s/\$mailto_1/$mailto_1/g;
		s/\$mailto_2/$mailto_2/g;
		s/\$mailto_3/$mailto_3/g;
		s/\$kanryo_url/$kanryo_url/g;
		s/\$sendmail_pas/$sendmail_pas/g;
		s/!passwd!/$passwd_form/;
		s/!checked1!/$checked1/;
		s/!checked2!/$checked2/;
		
		# シフトJISコード変換
		Jcode::convert(\$_, 'utf8');
		
		print "$_";
	}
	close(IN);

}

#------------------------------------------------------------------------------
# 予約通知（管理者宛）メール表示
#------------------------------------------------------------------------------
sub mail_admin{
	
	open (IN,"$db_mail_admin") || &error("$db_mail_adminが開けません。");
	while(<IN>){
		($admin_subject,$admin_mailformat) = split(/<>/);
	}
	close(IN);
	$admin_mailformat =~ s/<br>/\n/g;

	open (IN,"$skin_mail_admin") || &error("$skin_mail_adminが開けません。");
	&header;
	while(<IN>){
		$_ =~ s/\$admin_script/$admin_script/g;
		$_ =~ s/\$admin_subject/$admin_subject/g;
		$_ =~ s/\$admin_mailformat/$admin_mailformat/g;
		s/!passwd!/$passwd_form/;

		# シフトJISコード変換
		Jcode::convert(\$_, 'utf8');
		
		print "$_";
	}
	close(IN);

}

#------------------------------------------------------------------------------
# 予約確認（予約者宛）メール表示
#------------------------------------------------------------------------------
sub mail_henshin{
	
	open (IN,"$db_mail_henshin") || &error("$db_mail_henshinが開けません。");
	while(<IN>){
		($henshin_subject,$henshin_from_adress,$henshin_from_name,$henshin_mailformat) = split(/<>/);
	}
	close(IN);
	$henshin_mailformat =~ s/<br>/\n/g;

	open (IN,"$skin_mail_henshin") || &error("$skin_mail_henshinが開けません。");
	&header;
	while(<IN>){
		$_ =~ s/\$admin_script/$admin_script/g;
		$_ =~ s/\$henshin_subject/$henshin_subject/g;
		$_ =~ s/\$henshin_from_adress/$henshin_from_adress/g;
		$_ =~ s/\$henshin_from_name/$henshin_from_name/g;
		$_ =~ s/\$henshin_mailformat/$henshin_mailformat/g;
		s/!passwd!/$passwd_form/;
		
		# シフトJISコード変換
		Jcode::convert(\$_, 'utf8');
		
		print "$_";
	}
	close(IN);

}

#------------------------------------------------------------------------------
# 設定完了表示
#------------------------------------------------------------------------------
sub kanryo{
	
	#基本情報書き込み
	if($back_mode eq 'kihon'){
		
		#エラー処理
		&error("メール送信先（管理者）アドレス 1 が入力されていません。") unless($in{'mailto_1'});
		&error("メール送信先（管理者）アドレス 1 の入力が不正です。") if ($in{'mailto_1'} !~ /[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,6}$/);
		&error("メール送信先（管理者）アドレス 2 の入力が不正です。") if ($in{'mailto_2'} !~ /[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,6}$/ && $in{'mailto_2'});
		&error("メール送信先（管理者）アドレス 3 の入力が不正です。") if ($in{'mailto_3'} !~ /[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,6}$/ && $in{'mailto_3'});
		&error("完了画面URLが入力されていません。") unless($in{'kanryo_url'});
		&error("完了画面URLの入力が不正です。") if($in{'kanryo_url'} !~ /[0-9a-zA-Z]+/);
		&error("sendmailのパスが入力されていません。") unless($in{'sendmail_pas'});
		&error("sendmailのパスの入力が不正です。") if($in{'sendmail_pas'} !~ /[0-9a-zA-Z]+/);
			
		#書き込み
		open(OUT,">$db_kihon") || &error("$db_kihonが開けません。");
		print OUT "$in{'mailto_1'}<>$in{'mailto_2'}<>$in{'mailto_3'}<>$in{'kanryo_url'}<>$in{'sendmail_pas'}<>$in{'henshin_sign'}";
		close(OUT);
	}
	
	#予約通知（管理者宛）メール編集 書き込み
	if($back_mode eq 'mail_admin'){
		#エラー処理
		&error("メールサブジェクトが入力されていません。") unless($in{'admin_subject'});
		&error("メール内容が入力されていません。") unless($in{'admin_mailformat'});
		
		#書き込み
		open(OUT,">$db_mail_admin") || &error("$db_mail_adminが開けません。");
		print OUT "$in{'admin_subject'}<>$in{'admin_mailformat'}";
		close(OUT);
	}

	#予約確認（予約者宛）メール編集 書き込み
	if($back_mode eq 'mail_henshin'){
		#エラー処理
		&error("メールサブジェクトが入力されていません。") unless($in{'henshin_subject'});
		&error("メール送信元 アドレスが入力されていません。") unless($in{'henshin_from_adress'});
		&error("メール送信元 アドレスの入力が不正です。") if ($in{'henshin_from_adress'} !~ /[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,6}$/);
		&error("メール差出人名が入力されていません。") unless($in{'henshin_from_name'});
		&error("メール内容が入力されていません。") unless($in{'henshin_mailformat'});
		
		#書き込み
		open(OUT,">$db_mail_henshin") || &error("$db_mail_henshinが開けません。");
		print OUT "$in{'henshin_subject'}<>$in{'henshin_from_adress'}<>$in{'henshin_from_name'}<>$in{'henshin_mailformat'}";
		close(OUT);
	}
	

	open (IN,"$skin_kanryo") || &error("$skin_kanryoが開けません。");
	&header;
	while(<IN>){
		$_ =~ s/\$admin_script/$admin_script/g;
		$_ =~ s/\$back_mode/$back_mode/g;
		s/!passwd!/$passwd_form/;
		
		# シフトJISコード変換
		Jcode::convert(\$_, 'utf8');
		
		print "$_";
	}
	close(IN);
	exit;
}