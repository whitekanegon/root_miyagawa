#!/usr/bin/perl

#======================================================================================
#	基本メールフォーム CGI　v1.0　Directed By PenguinNoise J.KANEDA
#
#   メインプログラム
#======================================================================================

#------------------------------------------------------------------------------
# 基本設定
#------------------------------------------------------------------------------

#このプログラムのファイル名
$script = 'regist.cgi';

$ver = 'MailForm by PenguinNoise (c) 2004';

#------------------------------------------------------------------------------
# 外部ファイル取り込み
#------------------------------------------------------------------------------

require './setting.cgi';
require $cgilib;

use lib $lib;
use Jcode;


&decode;
&times;
&open_kihon;

if($mode eq 'check' || !$mode){
	&check;
}
elsif($mode eq 'kanryo'){
	&sendmail;
}

#------------------------------------------------------------------------------
# 確認ページ表示
#------------------------------------------------------------------------------

sub check{
	
	$gobi{'text'} = 'をご入力ください。';
	$gobi{'textarea'} = 'をご入力ください。';
	$gobi{'select'} = 'を選択してください。';
	$gobi{'radio'} = 'を選択してください。';
	

	while ( ($key,$val) = each(%in) ){
		#必須項目の抽出
		if($key =~ /^must([0-9]*):/){
			$num = sprintf("%d",$1);
			@must_item[$num] = $key."=".$val;
			next;
		}

		$val =~ s/－/-/g;
		next if($key eq 'Submit' || $key eq 'submit' || $key eq 'x' || $key eq 'y');
		$val = kanryo if($key eq 'mode');
		$hidden_area .= qq|<input type="hidden" name="$key" value="$val">\n|;
	}
	
	foreach (@must_item){
		($key,$val) = split("=");
		@must_key = split(":",$key);
		if($must_key[0] && $must_key[1] && $must_key[2]){
			&error_form($val.$gobi{$must_key[2]}) unless($in{$must_key[1]});
			if($must_key[1] eq 'email' || $must_key[1] eq 'email_confirm'){
				&error_form($val."の入力が不正です。") if ($in{$must_key[1]} !~ /[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,6}$/);
			}
			if($must_key[1] eq 'email_confirm'){
				&error_form("メールアドレス（確認）が一致しません。") if($in{'email'} ne $in{'email_confirm'});
			}
		}
	
	}
	
	open(IN,"$skin_check") || &error_form("$skin_checkが開けません。");
	while(<IN>){
		#スキンファイルにSSI記述がある場合
		if(/#include/){
			@kaiso = split(/\//,$ENV{'REQUEST_URI'});
			$kaiso = "";
			foreach (0 .. $#kaiso - 2){
				$kaiso .= "../";
			}
			($dummy1,$ssi_file,$dummy2) = split(/"/);
			$include_path = $kaiso.$ssi_file;
			open(INCLUDE,"$include_path") || &error_form("$include_pathが開けません。");
			while($inc_line = <INCLUDE>){
				Jcode::convert(\$inc_line, 'utf8');
				push(@check,$inc_line);
			}
			close(INCLUDE);
			next;
		}

		foreach $i (keys(%in)){
			if($i eq 'system' || $i eq 'asp' || $i eq 'internet' || $i eq 'website' || $i eq 'it' || $i eq 'portal'){
				unless($in{$i}){
					s/!$i!//g;
				}else{
					$in{$i}{$i} = $in{$i}."／";
					s/!$i!/$in{$i}{$i}/g;
				}
			}
			s/!$i!/&nbsp;/g unless($in{$i});
			s/!$i!/$in{$i}/g;
		}
		s/!script!/$script/g;
		s/<!--hidden_area-->/$hidden_area/g;
		s/!.*!/&nbsp;/g;
		
		# シフトJISコード変換
		Jcode::convert(\$_, 'utf8');
		
		push(@check,$_);
	}
	
	&header;
	print @check;
	exit;
}

#------------------------------------------------------------------------------
# メール送信
#------------------------------------------------------------------------------

sub sendmail{

	#通知（管理者宛）メール
	open(IN,"$db_mail_admin") || &error("$db_mail_adminが開けません。");
	while(<IN>){
		($admin_subject,$admin_mailformat) = split(/<>/);
	}
	close(IN);
	
	while(($key,$val) = each(%in)  ){
		$admin_subject =~ s/!$key!/$val/g;
		$admin_mailformat =~ s/!$key!/$val/g;
	}
	$admin_mailformat =~ s/<br>/\n/g;
	$admin_mailformat =~ s/!date!/$date1/g;
	$admin_mailformat =~ s/!AGENT!/$ENV{'HTTP_USER_AGENT'}/;
	$admin_mailformat =~ s/!REFERER!/$ENV{'HTTP_REFERER'}/;
	$admin_mailformat =~ s/!SERVER!/$ENV{'SERVER_NAME'}/;
	$admin_mailformat =~ s/!METHOD!/$ENV{'REQUEST_METHOD'}/;
	&get_host;
	$admin_mailformat =~ s/!ADDR!/$ENV{'REMOTE_ADDR'}/;
	$admin_mailformat =~ s/!.*!//g;
	
	$msub = &base64($admin_subject);
	
	# VERPsによるReturn-pathの書き換え
#	if($email){
#		&verps($email,$mailto_1);
#	}else{
#		&verps($mailto_1);
#		$email = "webmaster";
#	}
	

	# sendmail起動
#	open(MAIL,"| $sendmail_pas -t -f$v_sender") || &error_form("送信失敗: $!");
	open(MAIL,"| $sendmail_pas -t") || &error_form("送信失敗: $!");
	print MAIL "To: $mailto_1\n";
	print MAIL "From: $email\n";
	print MAIL "Cc: $mailto_2,$mailto_3\n";
	print MAIL "Subject: $msub\n";
	print MAIL "Date: $date2\n";
	print MAIL "MIME-Version: 1.0\n";
	print MAIL "Content-type: text/plain; charset=ISO-2022-JP\n";
	print MAIL "Content-Transfer-Encoding: 7bit\n";
	print MAIL "X-Mailer: $ver\n\n";
	Jcode::convert(\$admin_mailformat, "jis", "utf8");
	print MAIL $admin_mailformat;
	close(MAIL);
	
	#確認（申込者宛）メール
	if($henshin_sign eq 'on'){
		open(IN,"$db_mail_henshin") || &error("$db_mail_henshinが開けません。");
		while(<IN>){
			($henshin_subject,$henshin_from_adress,$henshin_from_name,$henshin_mailformat) = split(/<>/);
		}
		close(IN);

		while(($key,$val) = each(%in)  ){
			$henshin_subject =~ s/!$key!/$val/g;
			$henshin_mailformat =~ s/!$key!/$val/g;
		}

		$henshin_mailformat =~ s/<br>/\n/g;
		$henshin_mailformat =~ s/!date!/$date1/g;
		$henshin_mailformat =~ s/!.*!//g;
		
		$msub = &base64($henshin_subject);
		$mhenshin_from_name = &base64($henshin_from_name);

		# VERPsによるReturn-pathの書き換え
#		&verps($henshin_from_adress,$email);

		# sendmail起動
#		open(MAIL,"| $sendmail_pas -t -f$v_sender") || &error_form("送信失敗: $!");
		open(MAIL,"| $sendmail_pas -t") || &error_form("送信失敗: $!");
		print MAIL "To: $email\n";
		print MAIL "From: $mhenshin_from_name <$henshin_from_adress>\n";
		print MAIL "Subject: $msub\n";
		print MAIL "Date: $date2\n";
		print MAIL "MIME-Version: 1.0\n";
		print MAIL "Content-type: text/plain; charset=ISO-2022-JP\n";
		print MAIL "Content-Transfer-Encoding: 7bit\n";
		print MAIL "X-Mailer: $ver\n\n";
		Jcode::convert(\$henshin_mailformat, "jis", "utf8");
		print MAIL $henshin_mailformat;
		close(MAIL);
	}
	
	print "Location: $kanryo_url\n\n";
	
	exit;
}

sub verps {
	my $from = shift;
	my $to = shift;
	
	$from =~ m/(.+)\@(.+)/;
	my $v_email_local = $1;
	my $v_email_domain = $2;
	
	my $v_mailto_1 = $to;
	$v_mailto_1 =~ tr/\@/=/;
	
	$v_sender = $v_email_local."-".$v_mailto_1."\@".$v_email_domain;
}
	