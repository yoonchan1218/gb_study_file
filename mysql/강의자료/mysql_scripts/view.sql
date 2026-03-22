use dml;

create table tbl_member(
	id bigint unsigned auto_increment primary key,
	member_name varchar(255)
);

create table tbl_post(
	id bigint unsigned auto_increment primary key,
	post_content varchar(255),
	member_id bigint unsigned not null,
	constraint fk_post_member foreign key(member_id)
	references tbl_member(id)
);

create or replace view view_post_member as
(
	select p.*, m.member_name
	from tbl_member m join tbl_post p
	on m.id = p.member_id
);

select * from view_post_member;

`
