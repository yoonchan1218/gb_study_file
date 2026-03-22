package com.app.threetier.service.post;

import com.app.threetier.common.enumeration.FileContentType;
import com.app.threetier.domain.TagVO;
import com.app.threetier.dto.FileDTO;
import com.app.threetier.dto.PostDTO;
import com.app.threetier.dto.PostFileDTO;
import com.app.threetier.dto.TagDTO;
import com.app.threetier.repository.FileDAO;
import com.app.threetier.repository.PostDAO;
import com.app.threetier.repository.PostFileDAO;
import com.app.threetier.repository.TagDAO;
import com.app.threetier.util.DateUtils;
import lombok.NoArgsConstructor;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Transactional(rollbackFor = Exception.class)
public class PostService {
    private final PostDAO postDAO;
    private final TagDAO tagDAO;
    private final FileDAO fileDAO;
    private final PostFileDAO postFileDAO;

//    추가
    public void write(PostDTO postDTO, ArrayList<MultipartFile> multipartFiles) {
        String rootPath = "C:/file/";
        String todayPath = getTodayPath();
        String path = rootPath + todayPath;

        FileDTO fileDTO = new FileDTO();
        PostFileDTO postFileDTO = new PostFileDTO();

        postDAO.save(postDTO);
        postDTO.getTags().forEach(tagDTO -> {
            tagDTO.setPostId(postDTO.getId());
            tagDAO.save(tagDTO.toVO());
        });
        postFileDTO.setPostId(postDTO.getId());
        multipartFiles.forEach(multipartFile -> {
            if(multipartFile.getOriginalFilename().isEmpty()){
                return;
            }
            UUID uuid = UUID.randomUUID();
            fileDTO.setFilePath(todayPath);
            fileDTO.setFileSize(String.valueOf(multipartFile.getSize()));
            fileDTO.setFileOriginalName(multipartFile.getOriginalFilename());
            fileDTO.setFileName(uuid.toString() + "_" + multipartFile.getOriginalFilename());
            fileDTO.setFileContentType(multipartFile.getContentType().contains("image") ? FileContentType.IMAGE : FileContentType.OTHER);
            fileDAO.save(fileDTO);

            postFileDTO.setId(fileDTO.getId());
            postFileDAO.save(postFileDTO.toPostFileVO());

            File directory = new File(fileDTO.getFilePath());
            if(!directory.exists()){
                directory.mkdirs();
            }

            try {
                multipartFile.transferTo(new File(path, fileDTO.getFileName()));
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        });
    }

//    목록
    public List<PostDTO> list(){
        List<PostDTO> posts = postDAO.findAll();

        posts.forEach(postDTO -> {
            postDTO.setCreatedDatetime(DateUtils.toRelativeTime(postDTO.getCreatedDatetime()));
            postDTO.setTags(tagDAO.findAllByPostId(postDTO.getId())
                    .stream().map((tagVO) -> toTagDTO(tagVO)).collect(Collectors.toList()));
            postDTO.setPostFiles(postFileDAO.findAllByPostId(postDTO.getId()));
        });
        return posts;
    }

    public String getTodayPath(){
        return LocalDate.now().format(DateTimeFormatter.ofPattern("yyyy/MM/dd"));
    }

    public TagDTO toTagDTO(TagVO tagVO){
        TagDTO tagDTO = new TagDTO();

        tagDTO.setId(tagVO.getId());
        tagDTO.setPostId(tagVO.getPostId());
        tagDTO.setTagName(tagVO.getTagName());

        return tagDTO;
    }
}















