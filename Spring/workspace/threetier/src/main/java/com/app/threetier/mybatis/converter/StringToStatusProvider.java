package com.app.threetier.mybatis.converter;

import com.app.threetier.common.enumeration.Provider;
import com.app.threetier.common.enumeration.Status;
import org.springframework.core.convert.converter.Converter;
import org.springframework.stereotype.Component;

@Component
public class StringToStatusProvider implements Converter<String, Provider> {
    @Override
    public Provider convert(String source) {
        return Provider.getProvider(source);
    }
}
