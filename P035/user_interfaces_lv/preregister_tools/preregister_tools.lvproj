<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="18008000">
	<Item Name="My Computer" Type="My Computer">
		<Property Name="server.app.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.control.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="server.tcp.port" Type="Int">0</Property>
		<Property Name="server.tcp.serviceName" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.tcp.serviceName.default" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.vi.callsEnabled" Type="Bool">true</Property>
		<Property Name="server.vi.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="preregister_tools.vi" Type="VI" URL="../preregister_tools.vi"/>
		<Item Name="softest2-ico.ico" Type="Document" URL="../../../../../Users/andrz/OneDrive/Dokumenty/LabVIEW Data/Icon Templates/VI/3rd party/softest2-ico.ico"/>
		<Item Name="Dependencies" Type="Dependencies"/>
		<Item Name="Build Specifications" Type="Build">
			<Item Name="preregister_tools" Type="EXE">
				<Property Name="App_copyErrors" Type="Bool">true</Property>
				<Property Name="App_INI_aliasGUID" Type="Str">{E61C6C98-0F44-4EC7-8ABD-40E709D4DEEA}</Property>
				<Property Name="App_INI_GUID" Type="Str">{8C000C4F-0B1E-4D8A-8E15-93DD47718A8C}</Property>
				<Property Name="App_serverConfig.httpPort" Type="Int">8002</Property>
				<Property Name="Bld_autoIncrement" Type="Bool">true</Property>
				<Property Name="Bld_buildCacheID" Type="Str">{29F66808-D3BA-47E5-AC2E-6D29C3EF094F}</Property>
				<Property Name="Bld_buildSpecName" Type="Str">preregister_tools</Property>
				<Property Name="Bld_excludeInlineSubVIs" Type="Bool">true</Property>
				<Property Name="Bld_excludeLibraryItems" Type="Bool">true</Property>
				<Property Name="Bld_excludePolymorphicVIs" Type="Bool">true</Property>
				<Property Name="Bld_localDestDir" Type="Path">../builds</Property>
				<Property Name="Bld_localDestDirType" Type="Str">relativeToCommon</Property>
				<Property Name="Bld_modifyLibraryFile" Type="Bool">true</Property>
				<Property Name="Bld_previewCacheID" Type="Str">{9AC2337F-1680-408D-AD46-5EF95F15C646}</Property>
				<Property Name="Bld_version.build" Type="Int">1</Property>
				<Property Name="Bld_version.major" Type="Int">1</Property>
				<Property Name="Destination[0].destName" Type="Str">preregister_tools.exe</Property>
				<Property Name="Destination[0].path" Type="Path">../builds/NI_AB_PROJECTNAME.exe</Property>
				<Property Name="Destination[0].preserveHierarchy" Type="Bool">true</Property>
				<Property Name="Destination[0].type" Type="Str">App</Property>
				<Property Name="Destination[1].destName" Type="Str">Support Directory</Property>
				<Property Name="Destination[1].path" Type="Path">../builds/data</Property>
				<Property Name="DestinationCount" Type="Int">2</Property>
				<Property Name="Exe_iconItemID" Type="Ref">/My Computer/softest2-ico.ico</Property>
				<Property Name="Source[0].itemID" Type="Str">{FD7EBD83-8DB3-46EB-A60C-18361C798144}</Property>
				<Property Name="Source[0].type" Type="Str">Container</Property>
				<Property Name="Source[1].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[1].itemID" Type="Ref">/My Computer/preregister_tools.vi</Property>
				<Property Name="Source[1].sourceInclusion" Type="Str">TopLevel</Property>
				<Property Name="Source[1].type" Type="Str">VI</Property>
				<Property Name="SourceCount" Type="Int">2</Property>
				<Property Name="TgtF_companyName" Type="Str">Softest - Andrzej Czajka</Property>
				<Property Name="TgtF_fileDescription" Type="Str">preregister_tools</Property>
				<Property Name="TgtF_internalName" Type="Str">preregister_tools</Property>
				<Property Name="TgtF_legalCopyright" Type="Str">Copyright © 2023 Softest - Andrzej Czajka</Property>
				<Property Name="TgtF_productName" Type="Str">preregister_tools</Property>
				<Property Name="TgtF_targetfileGUID" Type="Str">{BC1F471E-F2D6-4CCC-A47B-9F67B94435FB}</Property>
				<Property Name="TgtF_targetfileName" Type="Str">preregister_tools.exe</Property>
				<Property Name="TgtF_versionIndependent" Type="Bool">true</Property>
			</Item>
		</Item>
	</Item>
</Project>
