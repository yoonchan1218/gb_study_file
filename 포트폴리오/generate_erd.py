"""
TryCatch ERD Generator - White background, IntelliJ style
Uses matplotlib to draw tables with FK relationships
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import os

# ── Color scheme (IntelliJ light theme style) ──
BG_COLOR = '#FFFFFF'
TABLE_HEADER_BG = '#4A86C8'
TABLE_HEADER_FG = '#FFFFFF'
TABLE_BODY_BG = '#F5F7FA'
TABLE_BORDER = '#B0B0B0'
PK_COLOR = '#D4A017'
FK_COLOR = '#6B8E23'
COL_COLOR = '#333333'
LINE_COLOR = '#888888'

FONT_SIZE_HEADER = 7
FONT_SIZE_COL = 5.5
COL_HEIGHT = 0.18
HEADER_HEIGHT = 0.28
TABLE_WIDTH = 2.8
PADDING = 0.08


def draw_table(ax, x, y, name, columns):
    """Draw a single table box. columns = [(col_name, col_type, is_pk, is_fk), ...]"""
    n = len(columns)
    total_h = HEADER_HEIGHT + n * COL_HEIGHT + PADDING

    # Table body background
    body = FancyBboxPatch(
        (x, y - total_h), TABLE_WIDTH, total_h,
        boxstyle="round,pad=0.02", facecolor=TABLE_BODY_BG,
        edgecolor=TABLE_BORDER, linewidth=0.8)
    ax.add_patch(body)

    # Header background
    header = FancyBboxPatch(
        (x, y - HEADER_HEIGHT), TABLE_WIDTH, HEADER_HEIGHT,
        boxstyle="round,pad=0.02", facecolor=TABLE_HEADER_BG,
        edgecolor=TABLE_BORDER, linewidth=0.8)
    ax.add_patch(header)

    # Table name
    ax.text(x + TABLE_WIDTH / 2, y - HEADER_HEIGHT / 2, name,
            fontsize=FONT_SIZE_HEADER, fontweight='bold', color=TABLE_HEADER_FG,
            ha='center', va='center', fontfamily='monospace')

    # Columns
    for i, (col_name, col_type, is_pk, is_fk) in enumerate(columns):
        cy = y - HEADER_HEIGHT - PADDING / 2 - (i + 0.5) * COL_HEIGHT
        prefix = ''
        color = COL_COLOR
        if is_pk:
            prefix = 'PK '
            color = PK_COLOR
        elif is_fk:
            prefix = 'FK '
            color = FK_COLOR
        label = f"{prefix}{col_name}"
        ax.text(x + 0.08, cy, label,
                fontsize=FONT_SIZE_COL, color=color, va='center',
                fontfamily='monospace', fontweight='bold' if is_pk else 'normal')
        ax.text(x + TABLE_WIDTH - 0.08, cy, col_type,
                fontsize=FONT_SIZE_COL - 0.5, color='#777777', va='center', ha='right',
                fontfamily='monospace')

    return total_h


def draw_relation(ax, x1, y1, x2, y2, style='-'):
    """Draw FK relationship line."""
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=LINE_COLOR,
                                lw=0.6, connectionstyle='arc3,rad=0.1'))


# ══════════════════════════════════════════
#  TABLE DEFINITIONS (abbreviated columns)
# ══════════════════════════════════════════

tables = {
    'tbl_member': [
        ('id', 'bigint', True, False),
        ('member_id', 'varchar', False, False),
        ('member_password', 'varchar', False, False),
        ('member_name', 'varchar', False, False),
        ('member_email', 'varchar', False, False),
        ('member_phone', 'varchar', False, False),
        ('address_id', 'bigint', False, True),
        ('member_status', 'enum', False, False),
        ('member_profile_file_id', 'bigint', False, True),
        ('created_datetime', 'datetime', False, False),
        ('updated_datetime', 'datetime', False, False),
    ],
    'tbl_individual_member': [
        ('id', 'bigint', True, True),
        ('individual_member_birth', 'date', False, False),
        ('individual_member_gender', 'enum', False, False),
        ('individual_member_education', 'varchar', False, False),
        ('individual_member_point', 'int', False, False),
        ('individual_member_level', 'int', False, False),
    ],
    'tbl_corp': [
        ('id', 'bigint', True, True),
        ('corp_company_name', 'varchar', False, False),
        ('corp_business_number', 'varchar', False, False),
        ('corp_ceo_name', 'varchar', False, False),
        ('corp_kind_id', 'bigint', False, True),
        ('corp_kind_small_id', 'bigint', False, True),
        ('corp_company_type', 'varchar', False, False),
        ('corp_establishment_date', 'date', False, False),
        ('corp_website_url', 'varchar', False, False),
    ],
    'tbl_oauth': [
        ('id', 'bigint', True, True),
        ('provider', 'enum', False, False),
    ],
    'tbl_address': [
        ('id', 'bigint', True, False),
        ('address_zipcode', 'varchar', False, False),
        ('address_province', 'varchar', False, False),
        ('address_city', 'varchar', False, False),
        ('address_district', 'varchar', False, False),
        ('address_detail', 'varchar', False, False),
    ],
    'tbl_file': [
        ('id', 'bigint', True, False),
        ('file_path', 'varchar', False, False),
        ('file_name', 'varchar', False, False),
        ('file_original_name', 'varchar', False, False),
        ('file_size', 'varchar', False, False),
        ('file_content_type', 'enum', False, False),
    ],
    'tbl_experience_program': [
        ('id', 'bigint', True, False),
        ('corp_id', 'bigint', False, True),
        ('experience_program_title', 'varchar', False, False),
        ('experience_program_level', 'varchar', False, False),
        ('experience_program_status', 'enum', False, False),
        ('experience_program_deadline', 'date', False, False),
        ('experience_program_job', 'varchar', False, False),
        ('experience_program_view_count', 'int', False, False),
    ],
    'tbl_apply': [
        ('id', 'bigint', True, False),
        ('experience_program_id', 'bigint', False, True),
        ('member_id', 'bigint', False, True),
        ('apply_status', 'enum', False, False),
        ('created_datetime', 'datetime', False, False),
    ],
    'tbl_challenger': [
        ('id', 'bigint', True, False),
        ('apply_id', 'bigint', False, True),
        ('challenger_status', 'enum', False, False),
    ],
    'tbl_feedback': [
        ('id', 'bigint', True, True),
        ('feedback_content', 'text', False, False),
    ],
    'tbl_qna': [
        ('id', 'bigint', True, False),
        ('individual_member_id', 'bigint', False, True),
        ('qna_title', 'varchar', False, False),
        ('qna_content', 'text', False, False),
        ('qna_view_count', 'int', False, False),
        ('qna_status', 'enum', False, False),
    ],
    'tbl_qna_comment': [
        ('id', 'bigint', True, False),
        ('qna_id', 'bigint', False, True),
        ('member_id', 'bigint', False, True),
        ('qna_comment_parent', 'bigint', False, True),
        ('qna_comment_content', 'text', False, False),
    ],
    'tbl_qna_likes': [
        ('id', 'bigint', True, False),
        ('member_id', 'bigint', False, True),
        ('qna_id', 'bigint', False, True),
    ],
    'tbl_qna_file': [
        ('id', 'bigint', True, True),
        ('qna_id', 'bigint', False, True),
    ],
    'tbl_skill_log': [
        ('id', 'bigint', True, False),
        ('member_id', 'bigint', False, True),
        ('experience_program_id', 'bigint', False, True),
        ('skill_log_title', 'varchar', False, False),
        ('skill_log_content', 'text', False, False),
        ('skill_log_view_count', 'int', False, False),
        ('skill_log_status', 'enum', False, False),
    ],
    'tbl_skill_log_comment': [
        ('id', 'bigint', True, False),
        ('skill_log_id', 'bigint', False, True),
        ('member_id', 'bigint', False, True),
        ('skill_log_comment_parent_id', 'bigint', False, True),
        ('skill_log_comment_content', 'text', False, False),
    ],
    'tbl_skill_log_likes': [
        ('id', 'bigint', True, False),
        ('member_id', 'bigint', False, True),
        ('skill_log_id', 'bigint', False, True),
    ],
    'tbl_skill_log_file': [
        ('id', 'bigint', True, True),
        ('skill_log_id', 'bigint', False, True),
    ],
    'tbl_tag': [
        ('id', 'bigint', True, False),
        ('tag_name', 'varchar', False, False),
        ('skill_log_id', 'bigint', False, True),
    ],
    'tbl_main_notification': [
        ('id', 'bigint', True, False),
        ('member_id', 'bigint', False, True),
        ('notification_type', 'enum', False, False),
        ('notification_title', 'varchar', False, False),
        ('notification_is_read', 'boolean', False, False),
        ('qna_id', 'bigint', False, True),
        ('experience_program_id', 'bigint', False, True),
        ('skill_log_id', 'bigint', False, True),
    ],
    'tbl_point_details': [
        ('id', 'bigint', True, False),
        ('individual_member_id', 'bigint', False, True),
        ('point_type', 'enum', False, False),
        ('point_amount', 'int', False, False),
        ('remaining_point_amount', 'int', False, False),
        ('payment_amount', 'int', False, False),
        ('payment_order_id', 'varchar', False, False),
        ('cancelled_datetime', 'datetime', False, False),
    ],
    'tbl_latest_watch_posting': [
        ('id', 'bigint', True, False),
        ('member_id', 'bigint', False, True),
        ('experience_program_id', 'bigint', False, True),
    ],
    'tbl_scrap_posting': [
        ('id', 'bigint', True, False),
        ('member_id', 'bigint', False, True),
        ('experience_program_id', 'bigint', False, True),
        ('scrap_status', 'enum', False, False),
    ],
    'tbl_report': [
        ('id', 'bigint', True, False),
        ('member_id', 'bigint', False, True),
        ('report_reason_code', 'int', False, False),
        ('report_status', 'enum', False, False),
    ],
    'tbl_corp_notification': [
        ('id', 'bigint', True, False),
        ('corp_id', 'bigint', False, True),
        ('notification_type', 'enum', False, False),
        ('notification_title', 'varchar', False, False),
        ('notification_is_read', 'boolean', False, False),
    ],
    'tbl_corp_team_member': [
        ('id', 'bigint', True, True),
        ('corp_id', 'bigint', False, True),
        ('corp_team_member_status', 'enum', False, False),
    ],
    'tbl_corp_invite': [
        ('id', 'bigint', True, False),
        ('corp_id', 'bigint', False, True),
        ('invite_email', 'varchar', False, False),
        ('invite_code', 'varchar', False, False),
        ('invite_status', 'enum', False, False),
    ],
    'tbl_corp_kind': [
        ('id', 'bigint', True, False),
        ('corp_kind_name', 'varchar', False, False),
    ],
    'tbl_corp_kind_small': [
        ('id', 'bigint', True, False),
        ('corp_kind_parent_id', 'bigint', False, True),
        ('corp_kind_small_name', 'varchar', False, False),
    ],
    'tbl_corp_logo_file': [
        ('id', 'bigint', True, True),
        ('corp_id', 'bigint', False, True),
    ],
    'tbl_address_program': [
        ('id', 'bigint', True, False),
        ('address_id', 'bigint', False, True),
        ('experience_program_id', 'bigint', False, True),
    ],
    'tbl_experience_program_file': [
        ('id', 'bigint', True, True),
        ('experience_program_id', 'bigint', False, True),
    ],
    'tbl_apply_file': [
        ('id', 'bigint', True, True),
        ('apply_id', 'bigint', False, True),
    ],
}

# FK relationships: (from_table, to_table)
relations = [
    ('tbl_individual_member', 'tbl_member'),
    ('tbl_corp', 'tbl_member'),
    ('tbl_oauth', 'tbl_member'),
    ('tbl_corp_team_member', 'tbl_member'),
    ('tbl_corp_team_member', 'tbl_corp'),
    ('tbl_member', 'tbl_address'),
    ('tbl_member', 'tbl_file'),
    ('tbl_corp', 'tbl_corp_kind'),
    ('tbl_corp', 'tbl_corp_kind_small'),
    ('tbl_corp_kind_small', 'tbl_corp_kind'),
    ('tbl_corp_invite', 'tbl_corp'),
    ('tbl_corp_logo_file', 'tbl_file'),
    ('tbl_corp_logo_file', 'tbl_corp'),
    ('tbl_corp_notification', 'tbl_corp'),
    ('tbl_experience_program', 'tbl_corp'),
    ('tbl_experience_program_file', 'tbl_file'),
    ('tbl_experience_program_file', 'tbl_experience_program'),
    ('tbl_address_program', 'tbl_address'),
    ('tbl_address_program', 'tbl_experience_program'),
    ('tbl_apply', 'tbl_experience_program'),
    ('tbl_apply', 'tbl_individual_member'),
    ('tbl_apply_file', 'tbl_file'),
    ('tbl_apply_file', 'tbl_apply'),
    ('tbl_challenger', 'tbl_apply'),
    ('tbl_feedback', 'tbl_challenger'),
    ('tbl_qna', 'tbl_individual_member'),
    ('tbl_qna_comment', 'tbl_qna'),
    ('tbl_qna_comment', 'tbl_member'),
    ('tbl_qna_likes', 'tbl_individual_member'),
    ('tbl_qna_likes', 'tbl_qna'),
    ('tbl_qna_file', 'tbl_file'),
    ('tbl_qna_file', 'tbl_qna'),
    ('tbl_skill_log', 'tbl_individual_member'),
    ('tbl_skill_log', 'tbl_experience_program'),
    ('tbl_skill_log_comment', 'tbl_skill_log'),
    ('tbl_skill_log_comment', 'tbl_member'),
    ('tbl_skill_log_likes', 'tbl_individual_member'),
    ('tbl_skill_log_likes', 'tbl_skill_log'),
    ('tbl_skill_log_file', 'tbl_file'),
    ('tbl_skill_log_file', 'tbl_skill_log'),
    ('tbl_tag', 'tbl_skill_log'),
    ('tbl_main_notification', 'tbl_individual_member'),
    ('tbl_point_details', 'tbl_individual_member'),
    ('tbl_latest_watch_posting', 'tbl_individual_member'),
    ('tbl_latest_watch_posting', 'tbl_experience_program'),
    ('tbl_scrap_posting', 'tbl_individual_member'),
    ('tbl_scrap_posting', 'tbl_experience_program'),
    ('tbl_report', 'tbl_individual_member'),
]

# ── Layout: manual grid positions ──
# (table_name, col, row) - col/row in grid units
layout = {
    # Row 0: Core
    'tbl_address':              (0, 0),
    'tbl_file':                 (0, 2),
    'tbl_member':               (1, 1),
    'tbl_individual_member':    (2, 0),
    'tbl_corp':                 (2, 2),
    'tbl_oauth':                (1, 3),
    # Row 1: Corp details
    'tbl_corp_kind':            (3, 3.5),
    'tbl_corp_kind_small':      (4, 3.5),
    'tbl_corp_invite':          (3, 2.5),
    'tbl_corp_team_member':     (2, 3.5),
    'tbl_corp_logo_file':       (1, 4),
    'tbl_corp_notification':    (3, 4.5),
    # Row 2: Experience & Apply
    'tbl_experience_program':   (4, 1),
    'tbl_apply':                (5, 0),
    'tbl_challenger':           (6, 0),
    'tbl_feedback':             (7, 0),
    'tbl_address_program':      (4, 0),
    'tbl_experience_program_file': (5, 2),
    'tbl_apply_file':           (6, 1),
    # Row 3: QnA
    'tbl_qna':                  (4, 4),
    'tbl_qna_comment':          (5, 4.5),
    'tbl_qna_likes':            (5, 3.5),
    'tbl_qna_file':             (4, 5),
    # Row 4: Skill Log
    'tbl_skill_log':            (6, 3),
    'tbl_skill_log_comment':    (7, 3.5),
    'tbl_skill_log_likes':      (7, 2.5),
    'tbl_skill_log_file':       (6, 4),
    'tbl_tag':                  (7, 4.5),
    # Row 5: Notification, Points, Engagement
    'tbl_main_notification':    (3, 0.5),
    'tbl_point_details':        (3, 1.5),
    'tbl_latest_watch_posting': (5, 1),
    'tbl_scrap_posting':        (6, 2),
    'tbl_report':               (2, 4.5),
}

COL_SPACING = 3.3
ROW_SPACING = 3.0


def main():
    fig, ax = plt.subplots(1, 1, figsize=(28, 18))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(-0.5, 8.5 * COL_SPACING)
    ax.set_ylim(-6.5 * ROW_SPACING, 1.5)
    ax.axis('off')
    ax.set_aspect('equal')

    # Title
    ax.text(8.5 * COL_SPACING / 2, 1.0, 'TRY-CATCH ERD',
            fontsize=16, fontweight='bold', ha='center', va='center',
            color='#333333', fontfamily='monospace')

    # Draw tables
    table_positions = {}  # table_name -> (center_x, top_y, height)
    for tname, cols in tables.items():
        if tname not in layout:
            continue
        grid_col, grid_row = layout[tname]
        x = grid_col * COL_SPACING
        y = -grid_row * ROW_SPACING
        h = draw_table(ax, x, y, tname, cols)
        table_positions[tname] = (x, y, h)

    # Draw relations
    for from_t, to_t in relations:
        if from_t not in table_positions or to_t not in table_positions:
            continue
        fx, fy, fh = table_positions[from_t]
        tx, ty, th = table_positions[to_t]

        # Connect from center-bottom of from to center-top of to (or side)
        fcx = fx + TABLE_WIDTH / 2
        fcy = fy - fh
        tcx = tx + TABLE_WIDTH / 2
        tcy = ty

        # If tables are on same row, connect sides
        if abs(fy - ty) < ROW_SPACING * 0.5:
            if fx < tx:
                x1, y1 = fx + TABLE_WIDTH, fy - fh / 2
                x2, y2 = tx, ty - th / 2
            else:
                x1, y1 = fx, fy - fh / 2
                x2, y2 = tx + TABLE_WIDTH, ty - th / 2
        else:
            x1, y1 = fcx, fcy
            x2, y2 = tcx, tcy

        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle='->', color=LINE_COLOR,
                                    lw=0.5, connectionstyle='arc3,rad=0.08',
                                    alpha=0.6))

    # Legend
    legend_x = 0.2
    legend_y = -17
    ax.text(legend_x, legend_y, 'PK', fontsize=7, color=PK_COLOR,
            fontweight='bold', fontfamily='monospace')
    ax.text(legend_x + 0.6, legend_y, '= Primary Key', fontsize=6,
            color='#555', fontfamily='monospace')
    ax.text(legend_x + 2.5, legend_y, 'FK', fontsize=7, color=FK_COLOR,
            fontweight='bold', fontfamily='monospace')
    ax.text(legend_x + 3.1, legend_y, '= Foreign Key', fontsize=6,
            color='#555', fontfamily='monospace')

    plt.tight_layout(pad=0.5)
    out_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'TRY-CATCH_ERD.png')
    plt.savefig(out_path, dpi=200, bbox_inches='tight',
                facecolor=BG_COLOR, edgecolor='none')
    plt.close()
    print(f'Saved: {out_path}')


if __name__ == '__main__':
    main()
